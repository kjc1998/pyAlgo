PYTHON := python
PIP := pip
VERSION := $(shell git describe --always --tags --long | $(PYTHON) gitdescribe2pep440.py 2> /dev/null || echo "0.0.0")

PKG_VERSION_FILE=__version__.py
VERSION_FILE=Versionfile

$(VERSION_FILE):
	@echo "$(VERSION)" > $@

$(PKG_VERSION_FILE):
	@echo "__version__ = '$(VERSION)'" > $@

versionfiles: $(VERSION_FILE) $(PKG_VERSION_FILE)

devinstall: versionfiles
	$(PIP) install -e .[test]

test: tests

tests:
	pytest -vv tests/

clean:
	rm -rf dist/*
	rm -rf pyalgo.egg-info
	rm -rf pip-wheel-metadata
	rm -rf $(PACKAGE_FILE)
	rm -f $(VERSION_FILE)
	rm -f $(PKG_VERSION_FILE)
	find . -type d -iname __pycache__ | xargs rm -rf
	find . -type f -iname '*.pyc' | xargs rm -rf
	rm -rf .pytest_cache
	rm -f .coverage
	rm -rf .mypy_cache

.PHONY: devinstall tests clean
