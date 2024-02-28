from api.v1.views import app_views
from models import storage
from flask import jsonify, send_file
import io

@app_views.route('documents/<string:user_id>', strict_slashes=False, methods=['GET'])
def user_docs(user_id):
    stud = storage.get('Student', user_id)
    docs = stud.documents
    return jsonify([value.to_dict() for value in docs.values()])

@app_views.route('/documents/stats/<string:user_id>', strict_slashes=False, methods=["GET"])
def user_stats(user_id):
    stud = storage.get('Student', user_id)
    return jsonify({'documents': len(stud.documents)})

@app_views.route('/documents/download/<string:user_id>/<string:doc_id>', strict_slashes=False, methods=['GET'])
def download_doc(user_id, doc_id):
    file = object()
    stud = storage.get('Student', user_id)
    for values in stud.documents.values():
        if values.to_dict().get('id') == doc_id:
            file = values.get_file()
    return send_file('/home/yeab/alx/TemariSync/return/' + file, as_attachment=True)
