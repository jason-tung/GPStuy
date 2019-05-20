import sqlite3
from hashlib import sha256

DATABASE = 'data/database.db' #from prospective of app.py

def setup():
    """Creates the database and adds the user account user_info table."""
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    command =  "CREATE TABLE IF NOT EXISTS user_info (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, guardian_email TEXT UNIQUE NOT NULL,"
    command += "password TEXT NOT NULL,"
    command += "period1 TEXT, period2 TEXT, period3 TEXT, period4 TEXT, period5 TEXT,"
    command += "period6 TEXT, period7 TEXT, period8 TEXT, period9 TEXT, period10 TEXT)"
    c.execute(command)
    db.commit()
    db.close()

#============================ Adding Into Database ============================

def add_user(name, email, guardian_email, password):
    '''Takes in the email and password and adds
    it into the database table "user_info".'''
    password = sha256(password.encode('utf-8')).hexdigest()
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    command = "INSERT INTO user_info (name, email, guardian_email, password)VALUES(?,?,?,?,?);"
    c.execute(command,(name, email, guardian_email, password))
    db.commit()
    db.close()
#============================ Getting From Database ============================

def get_email_list():
    '''Returns the list of all emails.'''
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    command = "SELECT email FROM user_info;"
    c.execute(command)
    output = c.fetchall()
    db.close()
    user_list = []
    for user in output:
        user_list.append(user[0])
    return user_list

def authenticate(email, pw):
    """Returns True if given email and password match. Otherwise return False."""
    pw = sha256(pw.encode('utf-8')).hexdigest()
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    command = "SELECT * FROM user_info WHERE email='{}' AND password='{}'".format( email, pw )
    c.execute(command)
    retBool = c.fetchone() != None
    db.close()

    return retBool

def getIDFromEmail(email):
    """Returns the primary key ID of an account given a email."""
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    command = "SELECT id FROM user_info WHERE email='{}'".format( email )
    c.execute(command)
    userID = c.fetchone()[0]
    db.close()

    return userID
