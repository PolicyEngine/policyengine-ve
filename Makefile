.PHONY: install test format changelog

install:
	pip install -e .[dev]

test:
	pytest policyengine_ve/tests/ -v
	policyengine-core test policyengine_ve/tests/policy/ -c policyengine_ve

format:
	black . -l 79

changelog:
	python .github/bump_version.py
	towncrier build --yes --version $$(python -c "import re; print(re.search(r'version = \"(.+?)\"', open('pyproject.toml').read()).group(1))")

debug:
	jupyter notebook
