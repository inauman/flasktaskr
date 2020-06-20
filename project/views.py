import sqlite3
from functools import wraps
from flask import Flask, flash, g, redirect, render_template, request, session, url_for

# config
app = Flask(__name__)
app.config.from_object('_config')

# helper functions
def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])

# decorator to enforce login for the protected pages
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# route handlers

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('Goodbye')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] \
            or request.form['password'] != app.config['PASSWORD']:
            error = "Invalid Credentials. Please try again."
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            flash('Welcome')
            return redirect(url_for('tasks'))
    return render_template('login.html')

@app.route('/tasks/')
@login_required
def tasks():

    g.db = connect_db()
    cursor = g.db.execute('select name, due_date, priorirty, task_id from tasks \
        where status=1')

    # let's use list comprehension with dict to populate the 
    # data from db query
    open_tasks = [
        dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3]) \
            for row in cursor.fetchall()
    ]

    cursor = g.db.execute('select name, due_date, priority, task_id from tasks \
        where status=0')

    closed_tasks = [
        dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3]) \
            for row in cursor.fetchall()
    ]

    g.db.close()

    return render_template('tasks.html',
        form=AddTaskForm(request.form),
        open_tasks=open_tasks,
        closed_tasks=closed_tasks
    )
    