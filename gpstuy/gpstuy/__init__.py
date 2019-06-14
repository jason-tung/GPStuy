import os, csv, time, sqlite3, json
from random import shuffle
from .util import mapsolver as ms
from .util import db_create
from .util import schedule
from json import dumps
from datetime import datetime, timedelta

from urllib.request import Request, urlopen

from flask import Flask, render_template, request, session, url_for, redirect, flash
from sqlite3 import IntegrityError

app = Flask(__name__)

app.secret_key = os.urandom(32)  # key for session
if not os.path.isfile("/var/www/gpstuy/gpstuy/data/database.db"):
    db_create.setup()


schedule.create_stuy_schedule()

db_create.setup()


@app.route('/')
def home():
    try:
        schedule.create_stuy_schedule()
        type = schedule.get_bell_schedule()
        current_p = schedule.get_current_period(type if type else "REGULAR")
        if session['id'] == db_create.getIDFromEmail("jwu29@stuy.edu"):
            return redirect(url_for("admin_features"))
        return render_template("home.html", name=db_create.get_user_by_id(session['id']),
                               periods=db_create.get_periods_from_id(session['id']), current_period=current_p)
    except KeyError:
        return render_template("home.html")


@app.route("/api_path/", methods=["GET", "POST"])
def api_path():
    a = request.args['loc1']
    b = request.args['loc2']
    pairpath = ms.path(a, b)
    # print(pairpath)
    try:
        return dumps(pairpath)
    except:
        return "poopy"


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
            return render_template("home.html", name=db_create.get_user_by_id(session['id']),
                                   periods=db_create.get_periods_from_id(session['id']))

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
    succ = db_create.authenticate(email, pw)
    if succ:
        session['id'] = db_create.getIDFromEmail(email)
        flash("Successfully logged in.")
        type = schedule.get_bell_schedule()
        current_p = schedule.get_current_period(type if type else "REGULAR")
        if (email == "jwu29@stuy.edu"):
            return redirect(url_for("admin_features"))
        return render_template("home.html", name=db_create.get_user_by_id(session['id']),
                               periods=db_create.get_periods_from_id(session['id']), current_period=current_p)
    else:
        flash("Password is incorrect.")
        return redirect(url_for('login'))


@app.route('/profile')
def profile():
    try:
        student_periods = db_create.get_periods_from_id(session['id'])
        return render_template("profile.html", name=db_create.get_user_by_id(session['id']), periods=student_periods)

    except KeyError:
        flash("You are not logged in.")
        return redirect(url_for("home"))


@app.route('/schedule_updater', methods=["GET", "POST"])
def schedule_updater():
    try:
        id = session['id']
        _name = db_create.get_user_by_id(id)
    except KeyError:
        flash("You are not logged in!!!")
        return redirect(url_for("home"))

    _periods = ["period1", "period2", "period3", "period4", "period5", "period6", "period7", "period8", "period9",
                    "period10"]
    for period in _periods:
        room = request.form.get(period)
        if room == "":
            db_create.remove_room(id, period)
        else:
            room = "'{0}'".format(room)
            db_create.insert_room(id, period, room)

    student_periods = db_create.get_periods_from_id(id)
    flash("Successfully updated rooms.")
    # return render_template("profile.html", name = _name, periods = student_periods)
    return redirect("/profile")

@app.route('/bell_schedule', methods=["GET", "POST"])
def bell_schedule():
    choice = request.form.get('schedule_choice')
    if not choice:
        choice = "REGULAR"
    list_periods = schedule.get_list_periods(choice)
    converted_periods = []
    current_p = schedule.get_current_period(choice)

    start_minute = str(list_periods[-1][1].minute) if list_periods[-1][1].minute >= 10 else '0' + str(
        list_periods[-1][1].minute)
    end_minute = str(list_periods[0][0].minute) if list_periods[0][0].minute >= 10 else '0' + str(
        list_periods[0][0].minute)
    start = str(list_periods[-1][1].hour) + ":" + start_minute + " AM" if list_periods[-1][1].hour / 12 <= 1 else str(
        list_periods[-1][1].hour % 12) + ":" + start_minute + " PM"
    end = str(list_periods[0][0].hour) + ":" + end_minute + " AM" if list_periods[0][0].hour / 12 <= 1 else str(
        list_periods[0][0].hour % 12) + ":" + end_minute + " PM"
    after_before_school = (start, end)

    t_day = datetime.now()
    t_day = schedule.get_current_weekday() + ", " + schedule.get_current_month() + " " + str(t_day.day) + ", " + str(
        t_day.year)
    day_type = schedule.get_bell_schedule()  # in the form CONFERENCE/HOMEROOM/REGULAR, A, B
    day_type = day_type + ", " + schedule.get_type_of_day() if day_type and schedule.get_type_of_day() else day_type
    for p in list_periods:
        start_minute = str(p[0].minute) if p[0].minute >= 10 else '0' + str(p[0].minute)
        end_minute = str(p[1].minute) if p[1].minute >= 10 else '0' + str(p[1].minute)
        start = str(p[0].hour) + ":" + start_minute + " AM" if p[0].hour / 12 <= 1 else str(
            p[0].hour % 12) + ":" + start_minute + " PM"
        end = str(p[1].hour) + ":" + end_minute + " AM" if p[1].hour / 12 <= 1 else str(
            p[1].hour % 12) + ":" + end_minute + " PM"

        converted_periods.append((start, end))
    try:
        return render_template("bell_schedule.html", name=db_create.get_user_by_id(session['id']), option=choice,
                               periods=converted_periods, current_period=current_p, buffer=after_before_school,
                               today=t_day, day_info=day_type)

    except KeyError:
        return render_template("bell_schedule.html", option=choice, periods=converted_periods, current_period=current_p,
                               buffer=after_before_school, today=t_day, day_info=day_type)


# Admin Stuff

@app.route('/admin_features', methods=["GET", "POST"])
def admin_features():  # Send mass emails, upload layouts of schools, see list of students, edit students schedules (i.e. change room number and teacher name)
    print(db_create.get_user_by_id(session['id']))
    if db_create.get_user_by_id(session['id'])[0] == 'admin':
        is_post = request.method == "POST"
        if is_post:
            if request.form['action'] == "Display":
                table = db_create.get_email_list()
                print(table)
                return render_template("admin.html", t=table)
            elif request.form['action'] == "Search":
                table = db_create.search(request.form['stud_name'])
                return render_template("admin.html", t=table)
            return render_template("admin.html")
        else:
            return render_template("admin.html")
    return redirect(url_for("home"))


if __name__ == "__main__":
    # app.debug = True
    app.run()
