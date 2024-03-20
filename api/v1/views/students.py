from api.v1.views import app_views
from models import storage
from flask import jsonify, send_file, abort, request, make_response
from flask_login import LoginManager
from models.student import Student

@app_views.route('/students/<string:student_id>', strict_slashes=False, methods=['GET'])
def get_student(student_id):
    student = storage.get('Student', student_id)
    if student is not None:
        return jsonify(student.to_dict())
    return abort(404)

@app_views.route('/students/register', strict_slashes=False, methods=['POST'])
def register_student():
    data = request.get_json()
    all_studs = storage.all('Student')
    for stud in all_studs.values():
        if stud.email == data['email']:
            return jsonify({"error": "email already exists"}), 400
    student = Student(**data)
    student.save()
    return jsonify(student.to_dict()), 201
