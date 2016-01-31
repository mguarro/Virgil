from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/split")
def split():
    return render_template('split.html')
    
@app.route("/graph")
def graph():
    return render_template('graph.html')



if __name__ == "__main__":
    app.run()
