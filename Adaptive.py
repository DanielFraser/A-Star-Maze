import heapq as hpq
from datetime import datetime

import numpy as np

import Utility
import ui

SIZE = 101
GOAL = [100, 100]
openList = []
knowledge = dict() # always empty at start
closed = []
finalPath = []
nodes = 0
paths = []

# updates map after agent moves
def updateMap(loc):
    for x in [[-1, 0], [1, 0], [0, -1], [0, 1], [0, 0]]:
        a = np.add(loc, x)
        a = list(a)
        if Utility.inRange(a, SIZE):
            currentMap[a[0], a[1]] = currentMap[a[0], a[1]] % 2


# expands each node around current and makes sure we haven't been
# there or isn't blocked
def createPossible(loc):
    locs = []
    global openList
    for x in [[-1,0], [1, 0], [0,-1], [0, 1]]:
        a = np.add(loc, x)
        a = list(a)
        if Utility.inRange(a, SIZE) and currentMap[a[0], a[1]] != 1 and not any(x.loc == a for x in openList) \
                and a not in closed:
                locs.append(a)
    return locs

# print path by starting at goal
def getPath(start, g, current):
    global knowledge
    for x in closed: # only update ones we went to
        knowledge[str(x)] = g - knowledge[str(x)]
    pathL = [current.loc]
    while current.loc != start:
        current = current.parent
        pathL.append(current.loc)
    pathL.reverse()
    return pathL


# finds a path using A*
def findPath(start):
    g = 0  # used for adaptive
    global openList
    global knowledge
    openList = []
    if str(start) in knowledge:
        node = Utility.Node(start, hi=knowledge[str(start)])
    else:
        node = Utility.Node(start, hi=Utility.distance(start, GOAL))
    hpq.heappush(openList, node)
    foundGoal = False
    current = None
    while openList: # while there are nodes to expand
        current = hpq.heappop(openList) # get next best position

        if current.loc == GOAL: # found goal
            g = current.g  # get final g
            foundGoal = True
            break

        knowledge[str(current.loc)] = current.g  # add node to knowledge list
        closed.append(current.loc)

        global nodes
        nodes += 1  # add 1 to total nodes expanded

        possibleMoves = createPossible(current.loc)  # get list of all possible nodes
        for x in possibleMoves:
            if str(x) in knowledge: # do we have previous knowledge of this location
                node = Utility.Node(x, current, current.g + 1, knowledge[str(x)])
            else:
                node = Utility.Node(x, current, current.g + 1, Utility.distance(x, GOAL))
            hpq.heappush(openList, node)  # add it to binary heap

    if foundGoal: # we managed to get to goal
        return getPath(start, g, current)
    else: # no possible path found
        return []

# move agent and remove fog of war
def moveAgent(path):
    global finalPath
    for y,x in enumerate(path):
        global finalPath
        if currentMap[x[0], x[1]] == 0:
            updateMap(x)  # remove fog of war
            global agent
            agent = x
            finalPath.append(x)
        else:
            finalPath = finalPath[:-1]
            global closed
            closed = [path[y-1]] # reset current path
            break

# main method for adaptive
def Start(start, goal, mapA, gui):
    startTime = datetime.now()
    global SIZE
    SIZE = len(mapA)
    global currentMap
    currentMap = mapA + 2
    global GOAL
    GOAL = goal
    global agent
    agent = start
    updateMap(agent)  # remove fog of war
    global nodes
    nodes = 0   # reset nodes expanded
    global finalPath
    while agent != goal: # until agent reaches goal
        path = findPath(agent)  # get path (need to create one for reverse)
        if path:  # if there is a path, move agent
            moveAgent(path)
        else:  # no path, unable to get to goal
            finalPath = []
            print("No path found")
            break
    global closed
    closed = [] # clear closed
    knowledge.clear() # clear knowledge
    if gui: # show gui if user wants
        ui.gui(currentMap, len(currentMap), start, goal, finalPath)
    return [nodes, datetime.now() - startTime, bool(finalPath), paths]