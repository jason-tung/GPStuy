import os, csv, time, sqlite3, json
from random import shuffle


from urllib.request import Request, urlopen

from flask import Flask, render_template, request, session, url_for, redirect, flash

from .util import db as db

app = Flask(__name__)

app.secret_key = os.urandom(32)  # key for session

@app.route('/')
def hello_world():
    if len(session) != 0:
        return render_template("home.html", logged=True, user=list(session.items())[0][0])
    return render_template("landing.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
