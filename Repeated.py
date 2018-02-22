import heapq as hpq
from datetime import datetime

import numpy as np

import Utility

startTime = datetime.now()
# redo closed list


# load in a test case
#ACTUAL = np.load('Mazes/maze01.npy')

ACTUAL = np.full((5, 5), 0, dtype=np.int8)
ACTUAL[1, 2] = 1
ACTUAL[2, 2] = 1
ACTUAL[3, 2] = 1
ACTUAL[2, 3] = 1
ACTUAL[3, 3] = 1
ACTUAL[4, 3] = 1
# create blank board
size = len(ACTUAL[0])
currentMap = np.full((size, size), 0, dtype=np.int8)
openList = []
closed = dict() # always empty at start
finalPath = []
nodes = 0

# updates map before planning route
def updateMap(loc):
    for x in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        a = np.add(loc, x)
        a = list(a)
        if Utility.inRange(a, size):
            currentMap[a[0], a[1]] = ACTUAL[a[0], a[1]]


# expands each node around current and makes sure we haven't been
# there or isn't blocked
def createPossible(loc):
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
        start = goal
    cur = current
    pathL = [cur.loc]
    while cur.loc != start:
        cur = cur.parent
        pathL.append(cur.loc)
    if not reverse:
        pathL.reverse()
    return pathL


# finds a path using A*
def findPath(start, reverse=False):
    global goal
    localGoal = goal
    if reverse:
        localGoal, start = start, localGoal # reverse the values for backwards
    global openList
    global closed
    if closed:
        openList = []
        hpq.heappush(openList, Utility.Node(start, hi=Utility.distance(start, localGoal)))
    else:
        hpq.heappush(openList, Utility.Node(start, gi=0, hi=Utility.distance(start, localGoal)))
    foundGoal = False
    current = None
    while openList:
        current = hpq.heappop(openList) # get next best position
        closed[str(current.loc)] = current.g  # add node to closed list

        if current.loc == localGoal: # found goal
            foundGoal = True
            break

        # print(current)
        global nodes
        nodes += 1

        possibleMoves = createPossible(current.loc)  # get list of all possible nodes
        for x in possibleMoves:
            node = Utility.Node(x, current, current.g + 1, Utility.distance(x, localGoal))
            hpq.heappush(openList, node) # add it to binary heap

    if foundGoal:
        return getPath(start, reverse, current)
    else:
        return []


# move agent and remove fog of war
def moveAgent(path):
    for y,x in enumerate(path):
        global finalPath
        if currentMap[x[0], x[1]] == 0:
            updateMap(x)  # remove fog of war
            global agent
            agent = x
            finalPath.append(x)
        else:
            finalPath = finalPath[:-1]
            closed.clear()
            closed[str(path[y-1])] = 0
            break

# main method TODO later
def AStar(start, goal, name, reverse, adaptive):
    a=0

# main method
if __name__ == '__main__':
    start = [0, 0]
    goal = [size - 1, size - 1]
    agent = start
    updateMap(agent)  # remove fog of war
    while agent != goal:
        path = findPath(agent) # get path (need to create one for reverse)
        if path:    # if there is a path, move agent
            moveAgent(path)
        else:   # no path, unable to get to goal
            finalPath = []
            print("No path found")
            break

    if finalPath:
        print("Final path = {}".format(finalPath))
    #ui.gui(currentMap)
    print("nodes = {}".format(nodes))
    print(datetime.now() - startTime)

#