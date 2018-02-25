import heapq as hpq
from datetime import datetime

import numpy as np

import Adaptive as A
import Utility
import ui

# load in a test case
size = 101
GOAL = [100, 100]
closed = set() # always empty at start
curPath = []
finalPath = []
nodes = 0

# updates map before planning route
def updateMap(loc):
    for x in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        a = np.add(loc, x)
        a = list(a)
        if Utility.inRange(a, size):
            currentMap[a[0], a[1]] = currentMap[a[0], a[1]] % 2


# expands each node around current and makes sure we haven't been
# there or isn't blocked
def createPossible(loc, openList):
    locs = []
    for x in [[-1,0], [1, 0], [0,-1], [0, 1]]:
        a = np.add(loc, x)
        a = list(a)
        if Utility.inRange(a, size) and currentMap[a[0], a[1]] != 1 and not any(x.loc == a for x in openList) \
                and not str(a) in closed:
                locs.append(a)
    return locs

# while we have nodes to go to

# print path by starting at goal
def getPath(start, reverse, current):
    if reverse:
        start = GOAL
    pathL = [current.loc]
    while current.loc != start:
        current = current.parent
        pathL.append(current.loc)
    if not reverse:
        pathL.reverse()
    return pathL


# finds a path using A*
def findPath(start, reverse=False):
    global GOAL
    localGoal = GOAL
    if reverse:
        localGoal, start = start, localGoal # reverse the values for backwards
    openList = []
    hpq.heappush(openList, Utility.Node(start, gi=0, hi=Utility.distance(start, localGoal), smallG=gSize))
    foundGoal = False
    current = None
    while openList:
        current = hpq.heappop(openList) # get next best position


        if current.loc == localGoal: # found goal
            foundGoal = True
            break

        closed.add(str(current.loc))  # add node to closed list

        # print(current)
        global nodes
        nodes += 1

        possibleMoves = createPossible(current.loc, openList)  # get list of all possible nodes
        for x in possibleMoves:
            node = Utility.Node(x, current, current.g + 1, Utility.distance(x, localGoal), smallG=gSize)
            hpq.heappush(openList, node) # add it to binary heap

    if foundGoal:
        return getPath(start, reverse, current)
    else:
        return []


# move agent and remove fog of war
def moveAgent(path):
    global finalPath
    for y,x in enumerate(path):
        #print(x)
        if currentMap[x[0], x[1]] != 1:  # only move to known free or unknown
            updateMap(x)  # remove fog of war
            global agent
            agent = x
            finalPath.append(x)
        else:
            closed.clear()
            break


def AStar(name, start = [0, 0], goal = [100, 100], reverse=False, adaptive=False, smallG = False):
    mapA = np.load(name).astype(np.int8)
    if adaptive and reverse:
        print("can't do it!")
    elif adaptive and not reverse:
        return A.Start(start, goal, mapA)
    else:
        return Start(start, goal, mapA, reverse, smallG)

def Start(start, goal, mapA, reverse, smallG):
    startTime = datetime.now()
    global gSize
    gSize = smallG
    global size
    size = len(mapA)
    global currentMap
    currentMap = mapA + 2
    global GOAL
    GOAL = goal
    global agent
    agent = start
    updateMap(agent)  # remove fog of war
    global nodes
    nodes = 0
    global finalPath
    while agent != goal:
        path = findPath(agent, reverse)  # get path (need to create one for reverse)
        # print(path)
        if path:  # if there is a path, move agent
            moveAgent(path)
        else:  # no path, unable to get to goal
            finalPath = []
            print("No path found")
            break

    closed.clear()
    # if finalPath:
    #     print("Final path = {}".format(finalPath))
    ui.gui(currentMap, len(currentMap), start, goal, finalPath)
    return [nodes, datetime.now() - startTime, bool(finalPath)]

# # main method
# if __name__ == '__main__':
#     AStar('Mazes/special.npy', [4,2], [4,4], adaptive=True)
#     AStar('Mazes/special.npy', [4, 2], [4, 4])
