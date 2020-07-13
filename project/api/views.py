# project/api/views.py

from datetime import datetime
from flask import flash, redirect, jsonify, \
    session, url_for, Blueprint, make_response, request

from project import db
from project.models import Task

################
#### config ####
################

api_blueprint = Blueprint('api', __name__)

##########################
#### helper functions ####
##########################

def open_tasks():
    return db.session.query(Task).filter_by(
        status='1').order_by(Task.due_date.asc())

def closed_tasks():
    return db.session.query(Task).filter_by(
        status='0').order_by(Task.due_date.asc())

################
#### routes ####
################

@api_blueprint.route('/api/v1/tasks/', methods=['GET', 'POST'])
def api_tasks():
    if request.method == 'GET':
        results = db.session.query(Task).limit(10).offset(0).all()
        json_results = []
        for result in results:
            data = {
                'task_id': result.task_id,
                'task name': result.name,
                'due date': str(result.due_date),
                'priority': result.priority,
                'posted date': str(result.posted_date),
                'status': result.status,
                'user id': result.user_id
                }
            json_results.append(data)
        return jsonify(items=json_results)
    elif request.method == 'POST':
        task_data = request.get_json()
        due_date = datetime.strptime(task_data['due_date'], '%m/%d/%Y').date()
        posted_date = datetime.strptime(task_data['posted_date'], '%m/%d/%Y').date()
        new_task = Task(
            task_data['name'],
            due_date,
            task_data['priority'],
            posted_date,
            task_data['status'],
            task_data['user_id']
        )
        db.session.add(new_task)
        db.session.commit()

        result = {"success": "Task successfully added"}
        code = 200

        return make_response(jsonify(result), code) 

@api_blueprint.route('/api/v1/tasks/<int:task_id>')
def task(task_id):
    result = db.session.query(Task).filter_by(task_id=task_id).first()
    if result:
        result = {
            'task_id': result.task_id,
            'task name': result.name,
            'due date': str(result.due_date),
            'priority': result.priority,
            'posted date': str(result.posted_date),
            'status': result.status,
            'user id': result.user_id
        }
        code = 200
    else:
        result = {"error": "Element does not exist"}
        code = 404
    return make_response(jsonify(result), code)
