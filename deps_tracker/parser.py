"""
    deps_tracker.parser
    Parse requirements.txt and setup.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import glob
import re
import os
import subprocess
import shutil
import tempfile


_line_re = re.compile(r'^([a-zA-Z0-9\-_\.]+)((===?|>=?|<=?|~=).*)?$')


class InvalidLineError(Exception):
    pass


class FailedSetupCall(Exception):
    pass


def _parse_line(line):
    """Return all the information contained in a specific line"""
    line = line.strip()  # Remove some whitespaces

    parsed = _line_re.match(line)
    if parsed is None:
        raise InvalidLineError("Line doesn't match")

    result = parsed.groups()
    package = result[0]
    specifier = None
    if len(result) > 1:
        specifier = result[1]

    return {"package": package, "specifier": specifier}


def parse_requirements(path):
    """Parse a requirements file"""
    path = os.path.expanduser(path)
    with open(path) as f:
        content = f.read()

    result = []
    for line in content.split("\n"):
        # Ignore empty lines
        if line.strip() == "":
            continue

        # CLI arguments are not supported
        if line[0] == "-":
            continue

        # Remove comments
        if "#" in line:
            line = line.split("#", 1)[0]

        try:
            result.append(_parse_line(line))
        except InvalidLineError:
            pass

    return result


def parse_setup(path):
    """Parse a setup.py file"""
    path = os.path.expanduser(path)

    tempdir = tempfile.mkdtemp()
    try:
        res = subprocess.call(["python3", path, "egg_info", "-e", tempdir],
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)

        # Return code != 0 means something went wrong
        if res != 0:
            raise FailedSetupCall("setup.py returned non-zero error code")

        # Since it's a new directory the only sub-directory should be the one
        # created by setuptools
        requirements = glob.glob(os.path.join(tempdir, "*", "requires.txt"))[0]
        with open(requirements) as f:
            content = f.read()

        result = []
        for line in content.split("\n"):
            result.append(_parse_line(line))

        return result

    # Be sure to remove the temp directory
    finally:
        shutil.rmtree(tempdir)
