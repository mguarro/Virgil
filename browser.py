from flask import Flask, request, redirect, url_for
from flask import render_template
import os
from werkzeug import secure_filename
from DoiInterface import *
import time

UPLOAD_FOLDER = 'database_builder/pdfs'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/prefetch-doi/')
def prefetch_doi():
    return render_template('countries.json')

@app.route("/graph/")
def graph():
    return render_template('graph.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files['pdf_file']
        if f:
            if allowed_file(f.filename):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], repr(time.time()).replace('.','')+".pdf")
                f.save(filepath)
                doi = extract_doi(os.path.abspath(filepath))
                #print(doi)
                if doi:
                    return redirect(url_for('split', doi=doi, view='summary'))
                else:
                    #TODO: Make cute error page
                    return render_template('index.html')
        elif request.doi:
            doi = search_doi(request.doi)
            if doi:
                return redirect(url_for('split', doi=doi, view='summary'))
        else:
            doi = search_doi_by_title(request.doi)
            if doi:
                return redirect(url_for('split', doi=doi, view='summary'))
    return render_template('index.html')

@app.route("/split/")
def split():
    return render_template('split.html')
    

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.debug = True
    app.run()
