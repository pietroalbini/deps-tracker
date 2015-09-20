"""
    deps_tracker.tracker
    Track dependencies versions and which one needs updates

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import datetime

import requests
import packaging.specifiers


PYPI_URL = "https://pypi.python.org/pypi"


class UnknowDependency(Exception):
    """A dependency wasn't found on PyPI"""


class Dependency:
    """Representation of a dependency"""

    def __init__(self, package):
        self.package = package
        self.needed_by = {}
        self.requires_updates = {}

        self.latest_update = -1
        self.latest_release = None

        self.get_status()

    def add_requirement(self, requirement):
        """Add a thing which requires this dependency"""
        package = requirement["package"]
        specifier = packaging.specifiers.Specifier(requirement["specifier"])
        file = requirement["file"]

        if package not in self.needed_by:
            self.needed_by[package] = {}

        self.needed_by[package][file] = specifier

        # Update the self.requires_updates
        if self.latest_release not in specifier:
            if package not in self.requires_updates:
                self.requires_updates[package] = []
            self.requires_updates[package].append()

    def get_status(self):
        """Get the dependency status from PyPI"""
        response = requests.get(PYPI_URL+"/"+self.package+"/json")
        if response.status_code >= 400:
            raise UnknowDependency("Can't find "+self.package+" on PyPI")
        content = response.json()

        self.latest_release = content["info"]["version"]
        uploaded = content["releases"][self.latest_release][0]["upload_time"]
        converted = datetime.datetime.strptime(uploaded, "%Y-%m-%dT%H:%M:%S")
        self.latest_update = converted.timestamp()
