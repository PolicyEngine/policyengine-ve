.PHONY: install test format

install:
	pip install -e .[dev]

test:
	pytest policyengine_ve/tests/ -v
	policyengine-core test policyengine_ve/tests/policy/ -c policyengine_ve

format:
	black . -l 79

debug:
	jupyter notebook
