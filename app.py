import os, csv, time, sqlite3, json
from random import shuffle
from util import mapsolver

from urllib.request import Request, urlopen

from flask import Flask, render_template, request, session, url_for, redirect, flash

app = Flask(__name__)

app.secret_key = os.urandom(32)  # key for session

@app.route('/')
def hello_world():
    return render_template("home.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
