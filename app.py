import os, csv, time, sqlite3, json
from random import shuffle
<<<<<<< HEAD
from util import mapsolver as ms
=======
from util import mapsolver, db_create
>>>>>>> da5184cc2f8defb64ed651fb5f1c72fc81d66592

from urllib.request import Request, urlopen

from flask import Flask, render_template, request, session, url_for, redirect, flash

app = Flask(__name__)

app.secret_key = os.urandom(32)  # key for session

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/api_path", methods=["GET"])
def path_api():
    a= request.args['loc1']
    b = request.args['loc2']
    return path(a,b)

@app.route('/test_api')
def test_api():
    return render_template("api_test.html")

@app.route('/register')
def register():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("home.html")

@app.route('/submit')
def submit():
    return render_template("home.html")

if __name__ == "__main__":
    db_create.setup()
    app.debug = True
    app.run()
