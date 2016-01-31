from flask import Flask, request, redirect, url_for
from flask import render_template
import os
from werkzeug import secure_filename
from DoiInterface import *

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/graph/")
def graph():
    return render_template('graph.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['pdf_file']
        if file:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                doi = extract_doi(filepath)
                return redirect(url_for('split', doi=doi))
        elif request.doi:
            doi = search_doi(request.doi)
            if doi:
                return redirect(url_for('split', doi=doi))
        else:
            doi = search_doi_by_title(request.doi)
            if doi:
                return redirect(url_for('split', doi=doi))
    return render_template('index.html')

@app.route("/split/")
def split():
    return render_template('split.html')
    

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run()
