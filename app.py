import os, csv, time, sqlite3, json
from random import shuffle


from urllib.request import Request, urlopen

from flask import Flask, render_template, request, session, url_for, redirect, flash

app = Flask(__name__)

app.secret_key = os.urandom(32)  # key for session

@app.route('/')
def hello_world():
    print(getmap(1))

def getmap(x):
    with open('maps/floor{0}'.format(x), 'r') as file:
        map_dict = {}
        map_dict["map"] = file.read()
        line_ary = map_dict["map"].split("\n")
        
        return data

def solvemap(asciimap,loc1,loc2):
    
    asciimap.replace(loc1,"S").replace(loc2,"E")
    
    
    
def path(loc1,loc2):
    floor1=loc1[0]
    floor2=loc2[0]
    coord1=loc1[1:]
    coord2=loc2[1:]
    if floor1 == floor2:
        getmap(floor1)
    else:
        
        
    
if __name__ == "__main__":
    app.debug = True
    app.run()
