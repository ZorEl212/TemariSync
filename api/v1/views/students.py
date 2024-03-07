from api.v1.views import app_views
from models import storage
from flask import jsonify, send_file, abort, request, make_response

@app_views.route('/students/<string:student_id>', strict_slashes=False, methods=['GET'])
def get_student(student_id):
    student = storage.get('Student', student_id)
    if student is not None:
        return jsonify(student.to_dict())
    return abort(404)
