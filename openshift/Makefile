.ONESHELL:
SHELL = /bin/bash

.PHONY: all test

test:
	pip install -r requirements.txt --extra-index-url http://do-prd-mvn-01.do.viaa.be:8081/repository/pypi-all/simple --trusted-host do-prd-mvn-01.do.viaa.be
	pytest -vvv --cov=./app --junit-xml=./tests/test_results.xml