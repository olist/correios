.PHONY: help

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -rf htmlcov/
	@rm -f coverage.xml
	@rm -f *.log

outdated: ## Show outdated dependencies
	@pip list --outdated --format=columns

install:
	pip install -U -r requirements-dev.txt

check-types:  ## Check type annotations
	mypy correios --ignore-missing-imports --follow-imports=skip

flake:
	flake8 --max-line-length=120 correios tests

isort:  ## Check imports
	isort --check --diff -tc -rc correios tests

fix-imports:  ## Fix imports
	isort -rc .

pyformat:
	black correios tests samples docs

lint: check-types flake isort ## Run code lint

test: clean lint  ## Run tests
	pytest -x -v

cov-test: clean lint  ## Run coverage tests
	pytest -x --cov=correios/ --cov-report=term-missing --cov-report=html:htmlcov

update-wsdl:  ## Update wsdl files
	@python correios/update_wsdl.py
