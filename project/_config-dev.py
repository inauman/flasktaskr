# project/config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'

# setting to enable protection against cross-site scripting.
WTF_CSRF_ENABLED = True
DEBUG = True
# this setting is used for enabling creation of cryptographic
# token to validate form. Used in conjunction w/ WTF_CSRF
SECRET_KEY = 'my_precious'

DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH