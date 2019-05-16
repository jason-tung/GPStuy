import sqlite3
from hashlib import sha256

DATABASE = 'data/database.db' #from prospective of app.py

def setup():
    """Creates the database and adds the user account user_info table."""
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    command =  "CREATE TABLE IF NOT EXISTS user_info (\
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                name TEXT NOT NULL,\
                email TEXT UNIQUE NOT NULL,\
                guardian_email TEXT UNIQUE NOT NULL,\
                username TEXT UNIQUE NOT NULL,\
                password TEXT NOT NULL),\
                period1 TEXT NOT NULL, period2 TEXT NOT NULL, period3 TEXT NOT NULL, period4 TEXT NOT NULL, period5 TEXT NOT NULL,\
                period6 TEXT NOT NULL, period7 TEXT NOT NULL, period8 TEXT NOT NULL, period9 TEXT NOT NULL, period10 TEXT NOT NULL)"
    c.execute(command)
    db.commit()
    db.close()

#============================ Adding Into Database ============================

def add_user(name, email, guardian_email, username, password):
    '''Takes in the username and password and adds
    it into the database table "user_info".'''
    password = sha256(password.encode('utf-8')).hexdigest()
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    command = "INSERT INTO user_info (name, email, guardian_email, username, password)VALUES(?,?,?,?,?);"
    c.execute(command,(name, email, guardian_email, username, password))
    db.commit()
    db.close()
#============================ Getting From Database ============================

def get_username_list():
    '''Returns the list of all usernames.'''
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    command = "SELECT username FROM user_info;"
    c.execute(command)
    output = c.fetchall()
    db.close()
    user_list = []
    for user in output:
        user_list.append(user[0])
    return user_list

def authenticate(username, pw):
    """Returns True if given username and password match. Otherwise return False."""
    pw = sha256(pw.encode('utf-8')).hexdigest()
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    command = "SELECT * FROM user_info WHERE username='{}' AND password='{}'".format( username, pw )
    c.execute(command)
    retBool = c.fetchone() != None
    db.close()

    return retBool

def getIDFromUsername(username):
    """Returns the primary key ID of an account given a username."""
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    command = "SELECT id FROM user_info WHERE username='{}'".format( username )
    c.execute(command)
    userID = c.fetchone()[0]
    db.close()

    return userID
