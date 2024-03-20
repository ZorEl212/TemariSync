from api.v1.views import app_views
from models import storage
from flask import jsonify, send_file, abort, request, make_response

@app_views.route('/departments/<string:department_id>', strict_slashes=False, methods=['GET'])
def get_department(department_id):
    department = storage.get('Department', department_id)
    if department is not None:
        return jsonify(department.to_dict())
    return abort(404)

@app_views.route('/departments', strict_slashes=False, methods=['GET'])
def get_departments():
    departments = storage.all('Department')
    return jsonify([value.to_dict() for value in departments.values()])
