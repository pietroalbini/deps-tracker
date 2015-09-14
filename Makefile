# BuildTheDocs's makefile
#
# Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
# Released under the MIT license

.PHONY: build install devel clean


# Package build

build: build/packages/*.tar.gz build/packages/*.whl

build/envs/build: requirements-build.txt
	@rm -rf build/envs/build
	@mkdir -p build/envs/build
	virtualenv -p python3 build/envs/build
	build/envs/build/bin/pip install -r requirements-build.txt

build/packages/*.tar.gz: build/envs/build deps_tracker/** setup.py
	@rm -f build/packages/*.tar.gz
	build/envs/build/bin/python3 setup.py sdist -d build/packages

build/packages/*.whl: build/envs/build deps_tracker/** setup.py
	@rm -rf build/packages/*.whl
	build/envs/build/bin/python3 setup.py bdist_wheel -d build/packages


# Installation

install: build/packages/*.whl
	python3 -m pip install --upgrade build/packages/*.whl


# Development tools

devel: deps_tracker.egg-info

build/envs/devel:
	@rm -rf build/envs/devel
	@mkdir -p build/envs/devel
	virtualenv -p python3 build/envs/devel

deps_tracker.egg-info: build/envs/devel setup.py
	build/envs/devel/bin/pip install -e .
	@touch deps_tracker.egg-info


# Cleanup

clean:
	@rm -rf build
	@rm -rf deps_tracker.egg-info


# Help message

help:
	@echo "Available targets:  (default is 'build')"
	@echo "- build       Create the .tar.gz and .whl packages"
	@echo "- install     Install deps-tracker in the current environment"
	@echo "- devel       Setup the development environment"
	@echo "- clean       Clean up the source directory"
