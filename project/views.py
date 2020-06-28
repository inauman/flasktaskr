
from functools import wraps
from flask import Flask, flash, g, redirect, render_template, request, \
    session, url_for
from project.forms import AddTaskForm, RegisterForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import datetime

# config
app = Flask(__name__)
app.config.from_object('project.config')
db = SQLAlchemy(app)

# this 'Model' can only be imported 
# after initializing the database
from project.models import Task, User

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
# logout
@app.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('Goodbye')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    error=None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['name']).first()
            if user is not None and user.password == request.form['password']:
                session['logged_in'] = True
                session['user_id'] = user.id
                flash('Welcome!')
                return redirect(url_for('tasks'))
            else:
                error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error)

# list tasks
@app.route('/tasks/')
@login_required
def tasks():
    return render_template('tasks.html',
        form=AddTaskForm(request.form),
        open_tasks=open_tasks(),
        closed_tasks=closed_tasks()
    )
    
# add new task
@app.route('/add/', methods=['POST'])
@login_required
def new_task():
    error = None
    form = AddTaskForm(request.form) 
    if request.method == 'POST':
        if form.validate_on_submit():
            new_task = Task(
                form.name.data, 
                form.due_date.data, 
                form.priority.data,
                datetime.datetime.utcnow(),
                '1',
                session['user_id']
            )
            db.session.add(new_task)
            db.session.commit()
            flash("New entry was successfully posted. Thanks.")
            return redirect(url_for('tasks'))
        else:
            return render_template('tasks.html', form=form, error=error)
    return render_template(
        'tasks.html', 
        form=form, 
        error=error,
        open_tasks=open_tasks(),
        closed_tasks=closed_tasks()
        )

    

# Mark task complete
@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().user_id:
        task.update({"status": "0"})
        db.session.commit()
        flash('The task is complete. Nice.')
        return redirect(url_for('tasks'))
    else:
        flash('You can only update tasks that belong to you.')
        return redirect(url_for('tasks'))

# delete tasks
@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] ==  task.first().user_id:
        task.delete()
        db.session.commit()
        flash('The task was deleted')
        return redirect(url_for('tasks'))
    else:
        flash('You can only delete tasks that belong to you.')
        return redirect(url_for('tasks'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    error=None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                form.name.data,
                form.email.data,
                form.password.data,
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Thanks for registering. Please login.')
                return redirect(url_for('login'))
            except IntegrityError:
                error = 'The username and/or email already exist.'
                return render_template('register.html', form=form, error=error)
    return render_template('register.html', form=form, error=error)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in the {getattr(form, field).label.text} field - {error}", 'error')

def open_tasks():
    return db.session.query(Task).filter_by(status='1', user_id=session['user_id']).order_by(Task.due_date.asc())

def closed_tasks():
    return db.session.query(Task).filter_by(status='0', user_id=session['user_id']).order_by(Task.due_date.asc())

