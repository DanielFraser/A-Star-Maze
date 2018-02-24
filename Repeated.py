import heapq as hpq
from datetime import datetime

import numpy as np

import Adaptive as A
import Utility

# redo closed list


# load in a test case
gSize = False
size = 101
currentMap = np.full((size, size), 0, dtype=np.int8)


# updates map before planning route
def updateMap(loc):
    for x in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        a = np.add(loc, x)
        a = list(a)
        if Utility.inRange(a, size):
            currentMap[a[0], a[1]] = currentMap[a[0], a[1]] % 2


# expands each node around current and makes sure we haven't been
# there or isn't blocked
def createPossible(loc, closed, openList):
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
    cur = current
    pathL = [cur.loc]
    while cur.loc != start:
        cur = cur.parent
        pathL.append(cur.loc)
    if not reverse:
        pathL.reverse()
    return pathL


# finds a path using A*
def findPath(start, closed, reverse=False):
    nodes = 0
    global GOAL
    localGoal = GOAL
    if reverse:
        localGoal, start = start, localGoal # reverse the values for backwards
    openList = []
    if closed:
        hpq.heappush(openList, Utility.Node(start, hi=Utility.distance(start, localGoal), smallG=gSize))
    else:
        hpq.heappush(openList, Utility.Node(start, gi=0, hi=Utility.distance(start, localGoal), smallG=gSize))
    foundGoal = False
    current = None
    while openList:
        current = hpq.heappop(openList) # get next best position
        closed.add(str(current.loc))  # add node to closed list

        if current.loc == localGoal: # found goal
            foundGoal = True
            break

        # print(current)
        nodes += 1

        possibleMoves = createPossible(current.loc, closed, openList)  # get list of all possible nodes
        for x in possibleMoves:
            node = Utility.Node(x, current, current.g + 1, Utility.distance(x, localGoal), smallG=gSize)
            hpq.heappush(openList, node) # add it to binary heap

    if foundGoal:
        return getPath(start, reverse, current), nodes
    else:
        return [], nodes


# move agent and remove fog of war
def moveAgent(path, closed, finalPath):
    for y,x in enumerate(path):
        if currentMap[x[0], x[1]] != 1:  # only move to known free or unknown
            updateMap(x)  # remove fog of war
            global agent
            agent = x
            finalPath.append(x)
        else:
            closed.clear()
            break


def AStar(name, start = [0, 0], goal = [100, 100], reverse=False, adaptive=False, smallG = False):
    mapA = np.load(name)
    if adaptive and reverse:
        print("can't do it!")
    elif adaptive and not reverse:
        return A.Start(start, goal, mapA)
    else:
        return Start(start, goal, mapA, reverse, smallG)

def Start(start, goal, mapA, reverse, smallG):
    startTime = datetime.now()
    closed = set()  # always empty at start
    finalPath = []
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
    nodes = 0
    while agent != goal:
        path, nodesT = findPath(agent, closed, reverse)  # get path (need to create one for reverse)
        nodes += nodesT
        if path:  # if there is a path, move agent
            moveAgent(path, closed, finalPath)
        else:  # no path, unable to get to goal
            finalPath = []
            print("No path found")
            break
        finalPath = finalPath[:-1]

    closed.clear()
    # if finalPath:
    #     print("Final path = {}".format(finalPath))
    # ui.gui(currentMap)
    return [nodes, datetime.now() - startTime]

# # main method
# if __name__ == '__main__':
#     AStar('Mazes/special.npy', [4,2], [4,4], adaptive=True)
#     AStar('Mazes/special.npy', [4, 2], [4, 4])
