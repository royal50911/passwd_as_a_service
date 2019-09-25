################
# Project: Password as a service 
# @Author: Hien Hoang
################
# Makefile helps to run the app easily
################
.PHONY: clean virtenv
.ONESHELL:

default: usage

usage:
	@echo 'Usage: make <target>'
	@echo '1/ make test --- running unit tests for api app'
	@echo '2/ make run_app --- start api app in background with output.log'
	@echo '3/ make deploy_app --- deploy app on virtual env'
	@echo '4/ make virtenv --- create virtual env for the app'
	@echo '5/ make clean --- clean up env and kill app if running'
	
virtenv:
	pip install virtualenv
	mkdir -p api_env
	virtualenv -p python3 api_env/venv
	source ./api_env/venv/bin/activate
	pip install -r requirements.txt
	
test:
	@echo Running unit tests ...
	pytest -v tests/test_restapi.py

run_app:
	@echo 'Making API App. It will be running in background ...'
	gunicorn api_app:app -b 0.0.0.0:8000 --access-logfile output.log &

deploy_app: clean virtenv
	. api_env/venv/bin/activate ; \
	gunicorn api_app:app -b 0.0.0.0:8000 --access-logfile output.log &

kill_app:
	pkill gunicorn
	rm -rf output.log

clean: kill_app
	rm -rf api_env
