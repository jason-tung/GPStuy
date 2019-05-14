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


def pprint(maze):
    print("".join(["".join([j for j in k]) + "\n" for k in maze]))


dirary = [[1, 0], [-1, 0], [0, 1], [0, -1]]


def solvemap(asciimap, loc1, loc2):
    testy = asciimap.split
    asciimap = asciimap.replace(loc1, "S").replace(loc2, "E")
    asciimap = "".join(['#' if k.islower() else k for k in asciimap])
    #print(asciimap)
    #print("----")
    asciimap_rows = asciimap.split('\n')
    mapary = [[k for k in j] for j in asciimap_rows]
    #pprint(mapary)

    def solve(row, col):
        nonlocal mapary
        if mapary[row][col] == 'E':
            return 1
        for dir in dirary:
            nrow = row + dir[0]
            ncol = col + dir[1]
            if mapary[nrow][ncol] in " E":
                if mapary[row][col] != "S":
                    mapary[row][col] = "@"
                solved = solve(nrow, ncol)
                if solved == -1:
                    mapary[nrow][ncol] = "."
                else:
                    return solved
        return -1

    for x in range(len(mapary)):
        for y in range(len(mapary[x])):
            if mapary[x][y] == "S":
                solve(x, y)
    return mapary


roommap = {"31": "a", "30": "b"}


def path(loc1, loc2):
    loc1,loc2=str(loc1),str(loc2)
    floor1 = loc1[0]
    floor2 = loc2[0]
    coord1 = loc1[1:]
    coord2 = loc2[1:]
    if floor1 == floor2:
        ans = solvemap(getmap(floor1)["map"], roommap[coord1], roommap[coord2])
        pprint(ans)
    else:
        return

path(131,130)

# with open('maps/floor{0}'.format(1), 'r') as file:
#     map_dict = {}
#     map_dict["map"] = file.read()
#     line_ary = map_dict["map"].split("\n")
#     map_dict["stairs"] = line_ary[0]
#     map_dict["map"] = "".join([k + "\n" for k in line_ary[1:]])[:-1]
#     solvemap(map_dict["map"], 'a', 'b')
