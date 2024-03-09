from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from flask import Flask, make_response, jsonify

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.teardown_appcontext
def teardown_st(Exception):
    storage.close()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": 'Not Found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001', threaded=True, debug=True)
