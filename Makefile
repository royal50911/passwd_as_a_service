################
# Project: Password as a service 
# @Author: Hien Hoang
################
# Makefile helps to run the app easily
################

test:
	@echo Running unit tests ...
	pytest -v tests/test_restapi.py
