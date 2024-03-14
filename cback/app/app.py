from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import threading
import time
from datetime import datetime
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@database:5432/cback1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255), nullable=False)
    scheduled_execution_time = db.Column(db.DateTime, nullable=False)
    task_type = db.Column(db.String(255), nullable=False)
    

    def __repr__(self):
        return f"<Task {self.id}: {self.task_name} - Scheduled at {self.scheduled_execution_time}>"

#  Support for CRUD operations: Create, read, update and delete tasks in the database


@app.route('/')
def index():
    return 'My Name is Nikhil'

@app.route('/tasks/create', methods=['POST'])
def create_task():
    data = request.get_json()
    print("hello")
    if 'task_name' not in data or 'scheduled_execution_time' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    new_task = Task(task_name=data['task_name'], scheduled_execution_time=data['scheduled_execution_time'], task_type=data['task_type'])
    print(new_task)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Task created successfully', 'task_id': new_task.id}), 201

@app.route('/tasks/detail', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    

    # Check if tasks list is empty
    if not tasks:
        # Return an error response if tasks list is empty
        error_message = {'error': 'No tasks found'}
        return jsonify(error_message), 404

    # If tasks list is not empty, construct the response
    result = [{'id': task.id, 'task_name': task.task_name, 'scheduled_execution_time': task.scheduled_execution_time, 'task_type': task.task_type } for task in tasks]
    return jsonify(result), 200

# Read a specific task by ID
@app.route('/tasks/get/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    result = {'id': task.id, 'task_name': task.task_name, 'scheduled_execution_time': task.scheduled_execution_time, 'task_type': task.task_type}
    return jsonify(result), 200


# Update a task by ID
@app.route('/tasks/update/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()

    if 'task_name' in data:
        task.task_name = data['task_name']
    if 'scheduled_execution_time' in data:
        task.scheduled_execution_time = data['scheduled_execution_time']
    if 'task_type' in data:
        task.task_type = data['task_type']
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'}), 200


@app.route('/tasks/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted successfully'}), 200


def execute_task(task):
    with app.app_context():
        print(f"Executing Task: {task.task_name} - Scheduled at: {task.scheduled_execution_time}")
        # Simulate work by sleeping for a random amount of time (e.g., between 1 and 5 seconds)
        import random
        sleep_time = random.uniform(1, 5)
        time.sleep(sleep_time)
        print(f"Task Completed: {task.task_name}")

def run_scheduler():
    with app.app_context():
        while True:
            current_time = datetime.now()
            tasks = Task.query.filter(Task.scheduled_execution_time <= current_time).order_by(Task.scheduled_execution_time).all()
            for task in tasks:
                execute_task(task)
                if(task.task_type == 'once'):  
                    db.session.delete(task)
                    db.session.commit()
                elif (task.task_type == 'daily'):
                    task.scheduled_execution_time = task.scheduled_execution_time + timedelta(days=1)
                    db.session.commit()
                elif (task.task_type == 'weekly'):
                    task.scheduled_execution_time = task.scheduled_execution_time + timedelta(weeks=1)
                    db.session.commit()
            time.sleep(1)

@app.route('/start')
def start_scheduler():
    threading.Thread(target=run_scheduler).start()
    return 'Scheduler started!'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)



