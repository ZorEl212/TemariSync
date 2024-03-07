from api.v1.views import app_views
from models import storage
from flask import jsonify, send_file, abort, request, make_response

@app_views.route('/courses/<string:course_id>', strict_slashes=False, methods=['GET'])
def get_course(course_id):
    course = storage.get('Course', course_id)
    if course is not None:
        return jsonify(course.to_dict())
    return abort(404)

@app_views.route('/courses/<string:course_id>/documents', strict_slashes=False, methods=['GET'])
def get_course_docs(course_id):
    course = storage.get('Course', course_id)
    if course is not None:
        return jsonify([value.to_dict() for value in course.documents.values()])
    return abort(404)
