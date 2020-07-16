# config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'my_precious'
    DEBUG = False
    TESTING = False 

    if os.environ.get('DATABASE_URL') is None:
        SQLALCHEMY_TRACK_MODIFICATIONS = False # This flag is required to turn off deprecation warning
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flasktaskr.db')
    else:
         SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEBUG = False
    DEVELOPMENT = False

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    DEBUG = False
    