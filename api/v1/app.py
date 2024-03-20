from random import random
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from flask import Flask, make_response, jsonify, request
from os import getenv
from flask_login import LoginManager, login_user

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(app)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@login_manager.user_loader
def load_user(user_id):
    return storage.get('Student', user_id)

app.config['SECRET_KEY'] = getenv('SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(app)
@app_views.route('/login', strict_slashes=False, methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    students = storage.all('Student')
    for student in students.values():
        if ((student.email == email or student.school_id == email) and student.password == password):
            login_user(student)
            return jsonify(student.to_dict())
    return make_response(jsonify({"error": "unauthorized"}), 401)

app.register_blueprint(app_views)
            
@app.teardown_appcontext
def teardown_st(Exception):
    storage.close()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": 'Not Found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001', threaded=True, debug=True)
