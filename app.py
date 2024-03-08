from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.route('/temarisync', strict_slashes=False)
@app.route('/temarisync/home', strict_slashes=False)
def index():
    return render_template('dashboard.html')

@app.route('/temarisync/docs/', strict_slashes=False)
def docs():
    return render_template('docs.html')

@app.route('/temarisync/docfile/', strict_slashes=False)
def docfile():
    return render_template('docInfo.html')

@app.route('/hello/', strict_slashes=False)
def hello():
    return render_template('hello.html')

@app.route('/temarisync/upload/', strict_slashes=False)
def upload():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')