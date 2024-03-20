from api.v1.views import app_views
from models import storage
from flask import jsonify, request, make_response, request
from flask_login import login_user, logout_user, current_user


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

@app_views.route('/logout', strict_slashes=False, methods=['POST'])
def logout():
    logout_user()
    return jsonify({"logout": "success"})

@app_views.route('/checkuser', strict_slashes=False, methods=['GET'])
def check_user():
    if current_user.is_authenticated:
        return jsonify(current_user.to_dict())
    else:
        return jsonify({"error": "unauthorized"}), 401