#!/usr/bin/env python3
""" 
Project: Password as a service 
@Author: Hien Hoang
################
configuration file for main app
"""

modes = {"dev":"DevelopmentConfig" ,
        "prod":"ProductionConfig",
        "testing":"TestingConfig"}
MODE = modes["dev"]
HOST = '0.0.0.0'
PORT = 8000
GROUP_FILE = "/etc/group"
PASSWD_FILE = "/etc/passwd"

# Class config modes for flask env    
class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    ENV = 'production'

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True

class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
