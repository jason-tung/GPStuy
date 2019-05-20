import os, csv, time, sqlite3, json
from random import shuffle
from util import mapsolver as ms
from util import db_create
from json import dumps

from urllib.request import Request, urlopen

from flask import Flask, render_template, request, session, url_for, redirect, flash

app = Flask(__name__)

app.secret_key = os.urandom(32)  # key for session

@app.route('/')
def home():

    return render_template("home.html", s = session, periods = ["TEST1", "TEST2"])

@app.route("/api_path/", methods=["GET", "POST"])
def api_path():
    a = request.args['loc1']
    b = request.args['loc2']
    pairpath = ms.path(a, b)
    #print(pairpath)
    return dumps(pairpath)

@app.route('/test_api', methods=["GET", "POST"])
def test_api():
    return render_template("api_test.html")

@app.route('/register')
def register():
    #db_create.add_user
    return render_template("register.html")

@app.route('/signup')
def sign_up():
    name = request.form("name")
    username = request.form("un")
    pw = request.form("pw")
    pwCon = request.form("pwCon")
    email = request.form("email")
    guardian_email = request.form("parEmail")
    if pw == pwCon:
        db_create.add_user(name, email, guardian_email, username, pw)

    else:
        flash('passwords do not match')
        return redirect(url_for(register))

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/auth')
def auth():
    email = request.form("email")
    pw = request.form("pw")
    succ = db_create.authenticate(email,pw)
    if succ:
            return redirect(url_for('home'))
    else:
        flash("passwords do not match")
        return redirect(url_for('login'))

@app.route('/submit')
def submit():
    return render_template("home.html")

if __name__ == "__main__":
    db_create.setup()
    app.debug = True
    app.run()
