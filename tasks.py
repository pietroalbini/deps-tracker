"""
    trackdeps's tasks file
    You should use this with invoke

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import os
import shutil
import glob
import re

import invoke


# This is because invoke can't keep backward compatibility...
_invoke_v = invoke.__version__.split(".")
if int(_invoke_v[0]) == 0 and int(_invoke_v[1]) <= 12:
    invoke.task = invoke.ctask


BASE = os.path.dirname(__file__)
PYTHON = "python3"
PROJECT = "trackdeps"


def create_env(name, requirements=False, self=False, force=False):
    """Create a new virtual environment"""
    path = os.path.join(BASE, "build", "envs", name)

    # Don't re-create the environment if force is False
    if os.path.exists(path):
        if force:
            shutil.rmtree(path)
        else:
            return path

    invoke.run("virtualenv -p %s %s" % (PYTHON, path))
    if requirements:
        invoke.run("%s/bin/pip install -r requirements-%s.txt" % (path, name))
    if self:
        invoke.run("%s/bin/pip install -e ." % path)

    return path


def remove_dir_content(path):
    """Remove the content of a directory"""
    for file in glob.glob(os.path.join(path, "*")):
        if os.path.isdir(file):
            shutil.rmtree(file)
        else:
            os.remove(file)


@invoke.task
def clean(ctx):
    """Clean all the build things"""
    for dir in "build", "%s.egg-info" % PROJECT:
        path = os.path.join(BASE, dir)
        if not os.path.exists(path):
            continue
        shutil.rmtree(path)

    exclude = ["%s/.git" % BASE, "%s/build" % BASE]
    remove_files = [re.compile(r'.py[co]$')]
    remove_dirs = [re.compile('__pycache__')]

    # Remove all the unwanted things
    for root, dirs, files in os.walk(BASE, topdown=False):
        # Skip excluded directories
        skip = False
        for one in exclude:
            if one == root or (root != BASE and one.startswith(root)):
                skip = True
                break
        if skip:
            continue

        # Remove all the unwanted files
        for file in files:
            file = os.path.join(root, file)
            for regex in remove_files:
                if regex.search(file):
                    os.remove(file)

        # Remove all the unwanted directories
        for dir in dirs:
            dir = os.path.join(root, dir)
            for regex in remove_dirs:
                if regex.search(dir):
                    shutil.rmtree(dir)


#
# Build and installation
#


@invoke.task
def devel(ctx):
    """Setup the development environment"""
    create_env("devel", self=True, force=True)


@invoke.task
def build(ctx):
    """Create a new build"""
    env = create_env("build", requirements=True)

    out = os.path.join(BASE, "build", "packages")
    if os.path.exists(out):
        remove_dir_content(out)

    for type in "sdist", "bdist_wheel":
        invoke.run("%s/bin/python setup.py %s -d %s" % (env, type, out))


@invoke.task(pre=[build])
def install(ctx):
    """Install the program on this environment"""
    invoke.run("python3 -m pip install --upgrade build/packages/*whl")


#
# Linting
#


@invoke.task
def lint(ctx):
    """Lint the source code"""
    env = create_env("lint", requirements=True)

    invoke.run("%s/bin/flake8 %s" % (env, PROJECT))


#
# Documentation
#


@invoke.task
def docs(ctx):
    """Build the documentation"""
    env = create_env("docs", requirements=True)

    docs_dir = os.path.join(BASE, "docs")
    build_dir = os.path.join(BASE, "build", "docs")
    remove_dir_content(build_dir)

    invoke.run("%s/bin/buildthedocs %s/buildthedocs.yml -o %s" %
               (env, docs_dir, build_dir))


#
# Pinned dependencies management
#


@invoke.task(name="deps-sync")
def deps_sync(ctx):
    """Sync dependencies versions"""
    env = create_env("tools", requirements=True)

    for env_name in os.listdir(os.path.join(BASE, "build", "envs")):
        req = os.path.join(BASE, "requirements-%s.txt" % env_name)
        if not os.path.exists(req):
            continue

        sub_env = os.path.join(BASE, "build", "envs", env_name)
        invoke.run("VIRTUAL_ENV=%s %s/bin/pip-sync %s/requirements-%s.txt"
                   % (sub_env, env, BASE, env_name), pty=True)


@invoke.task(name="deps-compile")
def deps_compile(ctx):
    """Compile new requirements-*.txt"""
    env = create_env("tools", requirements=True)

    for file in glob.glob(os.path.join(BASE, "requirements-*.in")):
        invoke.run("%s/bin/pip-compile %s > %s" % (env, os.path.abspath(file),
                   os.path.abspath(file)[:-3] + ".txt"))
