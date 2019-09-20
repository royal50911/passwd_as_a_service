################
# Project: Password as a service 
# @Author: Hien Hoang
################
# Makefile helps to run the app easily
################
## app mode : [dev, prod, testing]
MODE ?= dev

default: usage

usage:
	@echo 'Usage: make <target> <MODE=prod>'
	@echo '1/ make test --- running unit tests for api app'
	@echo '2/ make app MODE=dev(optional) --- start api app in background with output.log'
	@echo '3/ make kill_app --- kill api app in background and clean up output'
	
test:
	@echo Running unit tests ...
	pytest -v tests/test_restapi.py

app:
	@echo 'Making API App. It will be running in background ...'
	nohup python3 api_app.py -c $(MODE) > output.log &

kill_app:
	pkill -f api_app.py
	rm -f output.log
