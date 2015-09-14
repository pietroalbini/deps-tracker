"""
    deps_tracker.parser
    Parse requirements.txt and setup.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import re
import os


_line_re = re.compile(r'^([a-zA-Z0-9\-_\.]+)((===?|>=?|<=?|~=).*)?$')


class InvalidLineError(Exception):
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
