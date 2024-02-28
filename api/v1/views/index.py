from flask import jsonify
from api.v1.views import app_views, classes
from models import storage

@app_views.route('/status', strict_slashes=False)
def status():
    return jsonify({'status': 'OK'})

@app_views.route('/stats', strict_slashes=False)
def stats():
    return jsonify({key: storage.count(value) for key, value
                    in classes.items()})
