#!/usr/bin/python3


import setuptools

setuptools.setup(
    name = "deps-tracker",
    version = "1.0",
    url = "http://deps-tracker.pietroalbini.io",

    license = 'MIT',

    author = "Pietro Albini",
    author_email = "pietro@pietroalbini.io",

    install_requires = [
        'packaging',
        'setuptools',
        'jinja2',
        'pyyaml',
        'click',
    ],

    packages = [
        'deps_tracker',
    ],

    zip_safe = False,

    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Software Distribution",
    ],
)
