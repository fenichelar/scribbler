#!/usr/local/bin/python2

from myro import *
import csv

init("/dev/tty.scribbler")

def findEulerian(edges, verticies):
    def findEulerianFrom(edges, start):
        if len(edges) == 0:
            return [start]

        for edge in [i for i in edges if start in i]:
            (x, y) = edge
            path = findEulerianFrom([e for e in edges if e != edge], y if start == x else x)
            if path:
                return [start] + path
        return False

    for start in verticies:
        temp = findEulerianFrom(edges, start)
        if temp:
            return temp

verticies = {}
edges = []
coordinates = []
movementFactor = 100
mapFile = 'CS3630_Lab2_Map3.csv'

with open(mapFile, 'rb') as csvfile:
    contents = csv.reader(csvfile)
    mode = 0
    for row in contents:
        if len(row) == 0:
            mode = 1
        elif mode:
            edges.append((row[0],row[1]))
        else:
            verticies[row[0]] = (int(row[1]),int(row[2]))

path = findEulerian(edges,verticies)

print 'Path: ', path

wait(3)

for node in path:
    x = verticies[node][0] - verticies[path[0]][0]
    y = verticies[node][1] - verticies[path[0]][1]
    coordinates.append((x,y))
coordinates.pop(0)

for node in coordinates:
    moveTo(node[0]*movementFactor,node[1]*movementFactor)
