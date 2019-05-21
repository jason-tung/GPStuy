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
        return render_template("home.html", name = db_create.get_user_by_id(session['id']), periods = db_create.get_periods_from_id(session['id']))
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
            return render_template("home.html", name = db_create.get_user_by_id(session['id']), periods = db_create.get_periods_from_id(session['id']))

        except IntegrityError:
            flash('Email already in use. Please try again.')
            return redirect(url_for('register'))

    else:
        flash('Passwords do not match!')
        return redirect(url_for('register'))

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    try:
        session.pop('id')
        flash("Successfully logged out of your account")
        return render_template("home.html")
    except KeyError:
        flash("You are not logged in yet.")
        return render_template("home.html")


@app.route('/auth', methods=["GET", "POST"])
def auth():
    email = request.form.get("email")
    pw = request.form.get("pw")
    succ = db_create.authenticate(email,pw)
    if succ:
        session['id'] = db_create.getIDFromEmail(email)
        flash("Successfully logged in.")
        return render_template("home.html", name = db_create.get_user_by_id(session['id']), periods = db_create.get_periods_from_id(session['id']))
    else:
        flash("Password is incorrect.")
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    try:
        student_periods = db_create.get_periods_from_id(session['id'])
        return render_template("profile.html", name = db_create.get_user_by_id(session['id']), periods = student_periods)

    except KeyError:
        flash("You are not logged in.")
        return redirect(url_for("home"))

@app.route('/schedule_updater', methods=["GET", "POST"])
def schedule_updater():
    try:
        id = session['id']
        _name = db_create.get_user_by_id(id)

        _periods = ["period1", "period2", "period3", "period4", "period5", "period6", "period7", "period8", "period9", "period10"]

        for period in _periods:
            room = request.form.get(period)
            if room != "":
                db_create.insert_room(id, period, room)


        student_periods = db_create.get_periods_from_id(id)
        flash("Successfully updated rooms.")
        return render_template("profile.html", name = _name, periods = student_periods)
    except KeyError:
        flash("You are not logged in.")
        return redirect(url_for("home"))

if __name__ == "__main__":
    db_create.setup()
    app.debug = True
    app.run()
