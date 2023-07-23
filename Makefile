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
	$(PIP) install --upgrade build
	$(PYTHON) -m build

#' install: install package
install: package
	$(PIP) install $(PACKAGE_FILE)

#' devinstall: install package in development mode
devinstall: versionfile
	$(PIP) install -e .[test]

#' tests: alias for test
tests: test

#' test: unit tests + type checking
test: typecheck

#` unittest: run unit tests
unittest:
	pytest --verbose $(_EXTRA_ARGS) tests

#' typecheck: check type annotations
typecheck:
	pytest --verbose --mypy-config-file=mypy.ini tests

clean:
	rm -rf dist
	rm -rf pyalgo.egg-info
	rm -rf **/pyalgo.egg-info
	rm -rf pip-wheel-metadata
	rm -rf $(PACKAGE_FILE)
	rm -f $(VERSION_FILE)
	find . -type d -iname __pycache__ | xargs rm -rf
	find . -type f -iname '*.pyc' | xargs rm -rf
	rm -rf .pytest_cache
	rm -f .coverage
	rm -rf .mypy_cache

.PHONY: devinstall install tests clean versionfile package
