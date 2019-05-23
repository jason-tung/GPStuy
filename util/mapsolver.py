import os, csv, time, sqlite3, json
from random import shuffle

from urllib.request import Request, urlopen

from flask import Flask, render_template, request, session, url_for, redirect, flash

roommap = {"31": "a", "30": "b", "29": "c", "28":"d"}
stair_cost = {"0": 5, "1": 2, "2": 1, "3": 1}


def getmap(x):
    with open('maps/floor{0}'.format(x), 'r') as file:
        map_dict = {}
        map_dict["map"] = file.read()
        line_ary = map_dict["map"].split("\n")
        map_dict["stairs"] = line_ary[0].split(",")
        map_dict["map"] = "".join([k + "\n" for k in line_ary[1:]])[:-1]
        return map_dict


def pprint(maze):
    print("".join(["".join([j for j in k]) + "\n" for k in maze]))


dirary = [[1, 0], [-1, 0], [0, 1], [0, -1]]


def solvemap(asciimap, loc1, loc2):
    testy = asciimap.split
    asciimap = asciimap.replace(loc1, "S").replace(loc2, "E")
    asciimap = "".join(['#' if k.islower() else k for k in asciimap])
    # print(asciimap)
    # print("----")
    asciimap_rows = asciimap.split('\n')
    mapary = [[k for k in j] for j in asciimap_rows]

    # pprint(mapary)

    def solve(row, col, depth):
        nonlocal mapary
        if mapary[row][col] == 'E':
            return depth
        for dir in dirary:
            nrow = row + dir[0]
            ncol = col + dir[1]
            if mapary[nrow][ncol] in " E":
                if mapary[row][col] != "S":
                    mapary[row][col] = "@"
                solved = solve(nrow, ncol, depth + 1)
                if solved == -1:
                    mapary[nrow][ncol] = "."
                else:
                    return solved
        return -1

    cost = 0
    for x in range(len(mapary)):
        for y in range(len(mapary[x])):
            if mapary[x][y] == "S":
                cost = solve(x, y, 0)
    return (mapary, cost)


def get_sc(a, b, x):
    cost = stair_cost[x]
    a, b = int(a), int(b)
    return abs(a - b) * cost


def path(loc1, loc2):
    loc1, loc2 = str(loc1), str(loc2)
    floor1 = loc1[0]
    floor2 = loc2[0]
    coord1 = loc1[1:]
    coord2 = loc2[1:]
    if floor1 == floor2:
        ans = solvemap(getmap(floor1)["map"], roommap[coord1], roommap[coord2])[0]
        return {"f1": ans, "f2": ans}

        # pprint(ans[0])
    else:
        map1, map2 = getmap(floor1), getmap(floor2)
        shared_stairs = [k for k in map1["stairs"] if k in map2["stairs"]]

        def remap(map):
            nonlocal shared_stairs
            return "".join(['#' if l.isnumeric() and l not in shared_stairs else l for l in map])

        remap(map1["map"])
        remap(map2["map"])
        # print(map1["map"])
        least_cost = float("inf")
        bestpath = ()
        for x in shared_stairs:
            f1path = solvemap(map1["map"], roommap[coord1], x)
            f2path = solvemap(map2["map"], x, roommap[coord2])
            staircost = get_sc(floor1, floor2, x)
            this_cost = staircost + f1path[1] + f2path[1]
            least_cost = min(this_cost, least_cost)
            if this_cost <= least_cost:
                bestpath = (f1path[0], f2path[0])
        pprint(bestpath[1])
        return {"f1": bestpath[0], "f2": bestpath[1]}

# path(231, 130)

# with open('maps/floor{0}'.format(1), 'r') as file:
#     map_dict = {}
#     map_dict["map"] = file.read()
#     line_ary = map_dict["map"].split("\n")
#     map_dict["stairs"] = line_ary[0]
#     map_dict["map"] = "".join([k + "\n" for k in line_ary[1:]])[:-1]
#     solvemap(map_dict["map"], 'a', 'b')
