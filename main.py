import logging, sys
from flask import Flask, render_template, request

app = Flask(__name__)

keyword = ""

@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')

@app.route("/results", methods=['POST','GET'])
def results():
    if request.method == 'GET':
        return home()
    if request.method == 'POST':
        form_data = request.form
        keyword = form_data["textinput"]
        return render_template('results.html',form_data = form_data)

if __name__ =='__main__':
    app.run(debug=True)