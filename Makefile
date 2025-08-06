PYTHON := python
PIP := pip
VERSION := $(shell git describe --always --tags --long | $(PYTHON) gitdescribe2pep440.py 2> /dev/null || echo "0.0.0")
PKG_NAME := pyalgo
PACKAGE_FILE := dist/$(PKG_NAME)-$(VERSION).tar.gz

VERSION_FILE=Versionfile

$(VERSION_FILE):
	@echo "$(VERSION)" > $@

#' help: show this help
help:
	@echo "Available commands:"
	@echo "==================="
	@grep "^#' " $(_THIS_MAKEFILE) | sed -e "s/^#' //"


versionfile: $(VERSION_FILE)

#' package: build package
package: versionfile
	$(PIP) install --user --upgrade build
	$(PYTHON) -m build

#' install: install package
install: package
	$(PIP) install --user $(PACKAGE_FILE)

#' devinstall: install package in development mode
devinstall: versionfile
	$(PIP) install -e .
	$(PIP) install -r --user requirements-dev.txt

#' tests: alias for test
tests: test

#' test: unit tests + type checking
test: typecheck

#` unittest: run unit tests
unittest:
	pytest --verbose tests

#' typecheck: check type annotations
typecheck:
	mypy src \
		--config-file=mypy.ini \
		--strict
	pytest --verbose --mypy-config-file=mypy.ini tests

#' clean: remove all build, test, coverage and Python artifacts
clean: clean-build clean-pyc clean-test

#' clean-build: remove build artifacts'
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr $(VERSION_FILE)
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

#' clean-pyc: remove Python file artifacts
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

#' clean-test: remove test and coverage artifacts
clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -fr .mypy_cache

.PHONY: devinstall install tests clean clean-build clean-pyc clean-test versionfile package
