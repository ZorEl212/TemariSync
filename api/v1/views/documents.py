from api.v1.views import app_views
from models import storage
from flask import jsonify, send_file, abort, request, make_response
from models.document import Document
import os
import shutil

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

@app_views.route('/documents/upload/<string:user_id>', strict_slashes=False, methods=['POST'])
def upload_doc(user_id):
    if storage.get('Student', user_id):
        form_data = request.form
        file = request.files.get('file')
        doc = Document(**form_data)
        doc.tags = [tag.strip() for tag in form_data['tags'].split('#') if tag.strip()]
        os.mkdir(os.getenv('TEMP_DOC_DIR')  + doc.id)
        file.save(os.getenv('TEMP_DOC_DIR') + doc.id + "/" + file.filename)
        doc.save(os.getenv('TEMP_DOC_DIR')  + doc.id + '/' + file.filename)
        shutil.rmtree(os.getenv('TEMP_DOC_DIR')  + doc.id)
        return(doc.to_dict())
    abort(404)

@app_views.route('/documents/<string:user_id>/<string:doc_id>', strict_slashes=False, methods=['PUT'])
def update_doc(user_id, doc_id):
    stud = storage.get('Student', user_id)
    new_args = request.get_json() if request.is_json else abort(jsonify({'error': 'bad request'}), 400)
    if stud and f'Document.{doc_id}' in stud.documents.keys():
        doc = stud.documents.get(f"Document.{doc_id}")
        for key, value in new_args.items():
            setattr(doc, key, value)
            doc.save()
        return jsonify(doc.to_dict())
    return "Not Found"

@app_views.route('/documents/<string:user_id>/<string:doc_id>', strict_slashes=False, methods=['DELETE'])
def del_doc(user_id, doc_id):
    stud = storage.get('Student', user_id)
    if stud and f'Document.{doc_id}' in stud.documents.keys():
        storage.delete(stud.documents.get(f'Document.{doc_id}'))
        return make_response(jsonify({}), 204)
    return make_response(jsonify({'error': 'bad request'}), 400)
