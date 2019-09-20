
import os
basedir = os.path.abspath(os.path.dirname(__file__))
modes = {"dev":"DevelopmentConfig" ,
        "prod":"ProductionConfig",
        "testing":"TestingConfig"}
host = '0.0.0.0'
port = 5000

class SysFiles():
    GROUP_FILE = "/etc/group"
    PASSWD_FILE = "/etc/passwd"
    
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
