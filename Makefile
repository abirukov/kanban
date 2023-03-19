export PYTHONPATH := $(shell pwd):$(PYTHONPATH)

style:
	flake8 .
types:
	mypy .
tests:
	pytest --lf -vv --cov .
check:
	make style types tests
