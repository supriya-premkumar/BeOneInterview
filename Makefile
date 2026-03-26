PYTHON := .venv/bin/python
PIP := .venv/bin/pip

.PHONY: venv install check test

venv:
	python3 -m venv .venv

install: venv
	$(PIP) install -r requirements.txt

check:
	$(PYTHON) -c "import openpyxl, pytest; print('openpyxl', openpyxl.__version__); print('pytest', pytest.__version__)"

test:
	$(PYTHON) -m pytest
