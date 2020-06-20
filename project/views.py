import sqlite3
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for

# config
app = Flask(__name__)
app.config.from_object('_config')

# helper functions
def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

