################
# Project: Password as a service 
# @Author: Hien Hoang
################
# Makefile helps to run the app easily
################

default: usage

usage:
	@echo 'Usage: make <target>'
	@echo '1/ make test --- running unit tests for api app'
	@echo '2/ make app --- start api app in background with output.log'
	@echo '3/ make kill_app --- kill api app in background and clean up output'
	
test:
	@echo Running unit tests ...
	pytest -v tests/test_restapi.py

app:
	@echo 'Making API App. It will be running in background ...'
	gunicorn api_app:app -b 0.0.0.0:8000 --access-logfile output.log &

kill_app:
	pkill -f gunicorn
	rm -f output.log
