.PHONY: lint test

GECKO_VERSION := v0.23.0

setup:
	pip install -r requirements.txt
	pip install -r test-requirements.txt
	mkdir -p geckodriver
	wget -O- https://github.com/mozilla/geckodriver/releases/download/$(GECKO_VERSION)/geckodriver-$(GECKO_VERSION)-linux64.tar.gz | tar xzv -C geckodriver

lint:
	scripts/run-pylint.sh

test:
	@PATH="./geckodriver:$(PATH)" coverage run --source='.' manage.py test
