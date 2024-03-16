from api.v1.views import app_views
from models import storage
from flask import jsonify, send_file, abort, request, make_response
from models.document import Document
import os
import shutil
from flask import send_from_directory

@app_views.route('documents/<string:user_id>', strict_slashes=False, methods=['GET'])
def user_docs(user_id):
    stud = storage.get('Student', user_id)
    if (stud is None):
        abort(404)
    docs = stud.documents
    return jsonify([value.to_dict() for value in docs.values()])

@app_views.route('/documents/all', strict_slashes=False, methods=['GET'])
def all_docs():
    docs = storage.all('Document')
    return jsonify([value.to_dict() for value in docs.values()])

@app_views.route('/documents/details/<string:doc_id>', strict_slashes=False, methods=['GET'])
def get_doc(doc_id):
    doc = storage.get('Document', doc_id)
    if doc is not None:
        tags = [tag.name for tag in doc.tags]
        dict_doc = doc.to_dict()
        dict_doc['tags'] = tags
        return jsonify(dict_doc)
    return abort(404)

@app_views.route('/documents/stats/<string:user_id>', strict_slashes=False, methods=["GET"])
def user_stats(user_id):
    stud = storage.get('Student', user_id)
    return jsonify({'documents': len(stud.documents)})

@app_views.route('/documents/download/<string:user_id>/<string:doc_id>', strict_slashes=False, methods=['GET'])
def download_doc(user_id, doc_id):
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
    stud = storage.get('Student', user_id)
    if stud and f'Document.{doc_id}' in stud.documents.keys():
        storage.delete(stud.documents.get(f'Document.{doc_id}'))
        return make_response(jsonify({}), 204)
    return make_response(jsonify({'error': 'forbidden'}), 403)
