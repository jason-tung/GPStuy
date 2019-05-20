import os, csv, time, sqlite3, json
from random import shuffle
from util import mapsolver as ms
from util import db_create
from json import dumps

from urllib.request import Request, urlopen

from flask import Flask, render_template, request, session, url_for, redirect, flash
from sqlite3 import IntegrityError

app = Flask(__name__)

app.secret_key = os.urandom(32)  # key for session

@app.route('/')
def home():
    try:
        return render_template("home.html", name = db_create.get_user_by_id(session['id']))
    except KeyError:
        return render_template("home.html")


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
    return render_template("register.html")

@app.route('/signup', methods=["GET", "POST"])
def sign_up():
    name = request.form.get("name")
    pw = request.form.get("pw")
    pwCon = request.form.get("pwConfirm")
    email = request.form.get("email")
    guardian_email = request.form.get("parEmail")
    if pw == pwCon:
        try:
            db_create.add_user(name, email, guardian_email, pw)
            session['id'] = db_create.getIDFromEmail(email)
            flash('Account successfully created!')
            return render_template("home.html", name = db_create.get_user_by_id(session['id']))

        except IntegrityError:
            flash('Email already in use. Please try again.')
            return redirect(url_for('register'))

    else:
        flash('Passwords do not match!')
        return redirect(url_for('register'))

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/auth', methods=["GET", "POST"])
def auth():
    email = request.form.get("email")
    pw = request.form.get("pw")
    succ = db_create.authenticate(email,pw)
    if succ:
        session['id'] = db_create.getIDFromEmail(email)
        flash("Successfully logged in.")
        return render_template("home.html", name = db_create.get_user_by_id(session['id']))
    else:
        flash("Password is incorrect.")
        return redirect(url_for('login'))

@app.route('/submit')
def submit():
    return render_template("home.html")

if __name__ == "__main__":
    db_create.setup()
    app.debug = True
    app.run()
