import os, csv, time, sqlite3, json
from random import shuffle

from urllib.request import Request, urlopen

from flask import Flask, render_template, request, session, url_for, redirect, flash


def getmap(x):
    with open('maps/floor{0}'.format(x), 'r') as file:
        map_dict = {}
        map_dict["map"] = file.read()
        line_ary = map_dict["map"].split("\n")
        map_dict["stairs"] = line_ary[0]
        return map_dict


def solvemap(asciimap, loc1, loc2):
    print(asciimap)
    print("----")
    asciimap = asciimap.replace(loc1, "S").replace(loc2, "E")
    print(asciimap)
    print("----")
    asciimap = "".join(['#' if k.islower() else k for k in asciimap])
    asciimap_rows = asciimap.split('\n')
    mapary = [[k for k in j] for j in asciimap_rows]
    print(mapary)


def path(loc1, loc2):
    floor1 = loc1[0]
    floor2 = loc2[0]
    coord1 = loc1[1:]
    coord2 = loc2[1:]
    if floor1 == floor2:
        getmap(floor1)
    else:
        return


with open('maps/floor{0}'.format(1), 'r') as file:
    map_dict = {}
    map_dict["map"] = file.read()
    line_ary = map_dict["map"].split("\n")
    map_dict["stairs"] = line_ary[0]
    map_dict["map"] = "".join([k + "\n" for k in line_ary[1:]])[:-1]
    solvemap(map_dict["map"], 'a', 'b')