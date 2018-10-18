.PHONY: lint test

setup:
	pip install -r requirements.txt
	pip install -r test-requirements.txt
	mkdir -p geckodriver
	wget -O- https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz | tar xzv -C geckodriver

lint:
	scripts/run-pylint.sh

test:
	PATH="./geckodriver:$(PATH)" coverage run --source='.' manage.py test
