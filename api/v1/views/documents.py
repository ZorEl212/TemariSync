#!/usr/bin/env python3
"""Module for documents view
endpoints:
    - user_docs: GET /documents/<string:user_id>
    - all_docs: GET /documents/all
    - get_doc: GET /documents/details/<string:doc_id>
    - user_stats: GET /documents/stats/<string:user_id>
    - download_doc: GET /documents/download/<string:user_id>/<string:doc_id>
    - upload_doc: POST /documents/upload/<string:user_id>
    - update_doc: PUT /documents/<string:user_id>/<string:doc_id>
    - del_doc: DELETE /documents/<string:user_id>/<string:doc_id>
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, send_from_directory, abort, request, make_response
from models.document import Document
import os
import shutil


@app_views.route('documents/<string:user_id>', strict_slashes=False, methods=['GET'])
def user_docs(user_id):
    """GET /documents/<string:user_id> endpoint
    Return all documents for a user"""

    stud = storage.get('Student', user_id)
    docs = stud.documents if stud is not None else abort(404)
    return jsonify([value.to_dict() for value in docs])

@app_views.route('/documents/all', strict_slashes=False, methods=['GET'])
def all_docs():
    """GET /documents/all endpoint
    Return all documents in the database"""

    docs = storage.all('Document')
    return jsonify([value.to_dict() for value in docs.values()])

@app_views.route('/documents/details/<string:doc_id>', strict_slashes=False, methods=['GET'])
def get_doc(doc_id):
    """GET /documents/details/<string:doc_id> endpoint
    Return details of a document"""

    doc = storage.get('Document', doc_id)
    if doc is not None:
        tags = [tag.name for tag in doc.tags]
        dict_doc = doc.to_dict()
        dict_doc['tags'] = tags
        return jsonify(dict_doc)
    return abort(404)

@app_views.route('/documents/stats/<string:user_id>', strict_slashes=False, methods=["GET"])
def user_stats(user_id):
    """GET /documents/stats/<string:user_id> endpoint
    Return the number of documents for a user"""

    stud = storage.get('Student', user_id)
    return jsonify({'documents': len(stud.documents)})

@app_views.route('/documents/download/<string:user_id>/<string:doc_id>', strict_slashes=False, methods=['GET'])
def download_doc(user_id, doc_id):
    """GET /documents/download/<string:user_id>/<string:doc_id> endpoint
    Download a document from the server"""

    file = object()
    stud = storage.get('Student', user_id)
    for values in stud.documents:
        if values.to_dict().get('id') == doc_id:
            file = values.get_file()
            directory = os.getenv('RETURN_DIR')
            filename = values.title + values.file_type.lower()
            return send_from_directory(directory, file, as_attachment=True)
    abort(404)

@app_views.route('/documents/upload/<string:user_id>', strict_slashes=False, methods=['POST'])
def upload_doc(user_id):
    """POST /documents/upload/<string:user_id> endpoint
    Upload a document to the server"""

    if storage.get('Student', user_id):
        form_data = dict(request.form)
        file = request.files['file']
        tags = [tag.strip() for tag in form_data['tags'].split('#') if tag.strip()]
        form_data.pop('tags')
        doc = Document(**form_data)
        os.makedirs(os.getenv('TEMP_DOC_DIR')  + doc.id)
        file.save(os.getenv('TEMP_DOC_DIR') + doc.id + "/" + file.filename)
        doc.save(os.getenv('TEMP_DOC_DIR')  + doc.id + '/' + file.filename, tags=tags)
        shutil.rmtree(os.getenv('TEMP_DOC_DIR')  + doc.id)
        return(doc.to_dict())
    abort(404)

@app_views.route('/documents/<string:user_id>/<string:doc_id>', strict_slashes=False, methods=['PUT'])
def update_doc(user_id, doc_id):
    """PUT /documents/<string:user_id>/<string:doc_id> endpoint
    Update a document in the database"""

    stud = storage.get('Student', user_id)
    new_args = request.get_json() if request.is_json else abort(jsonify({'error': 'bad request'}), 400)
    if stud and doc_id in [d.id for d in stud.documents]:
        doc = storage.get('Document', doc_id)
        for key, value in new_args.items():
            setattr(doc, key, value) if key not in ['id', 'tags'] else None
        tags = [tag.strip() for tag in new_args['tags'].split('#') if tag.strip()]
        doc.save(tags=tags)
        return jsonify(doc.to_dict())
    return make_response(jsonify({'error': 'forbidden'}), 403)

@app_views.route('/documents/<string:user_id>/<string:doc_id>', strict_slashes=False, methods=['DELETE'])
def del_doc(user_id, doc_id):
    """DELETE /documents/<string:user_id>/<string:doc_id> endpoint
    Delete a document from the database"""

    stud = storage.get('Student', user_id)
    if stud and doc_id in [d.id for d in stud.documents]:
        storage.delete(storage.get('Document', doc_id))
        return make_response(jsonify({'delete': 'OK'}), 204)
    
    return make_response(jsonify({'error': 'forbidden'}), 403)
