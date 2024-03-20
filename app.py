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

@app.route('/temarisync/editdoc/', strict_slashes=False)
def editDoc():
    return render_template('editDoc.html')

@app.route('/temarisync/upload/', strict_slashes=False)
def upload():
    return render_template('upload.html')

@app.route('/temarisync/login/', strict_slashes=False)
def login():
    return render_template('login.html')

@app.route('/temarisync/register/', strict_slashes=False)
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')