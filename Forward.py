import heapq as hpq

import numpy as np

import Utility
import ui

# redo closed list

size = 101
# load in a test case
ACTUAL = np.load('Mazes/maze01.npy')
#ACTUAL = np.full((size, size), 0, dtype=np.int8)
# create blank board
currentMap = np.full((size, size), 0, dtype=np.int8)
openList = []
closed = []  # always empty at start
finalPath = []
nodes = 0

# updates map before planning route
def updateMap(loc):
    for x in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        a = np.add(loc, x)
        a = list(a)
        if (Utility.inRange(a, size)):
            currentMap[a[0], a[1]] = ACTUAL[a[0], a[1]]

# expands each node around current and makes sure we haven't been
# there or isn't blocked
def createPossible(loc, adaptive=False):
    locs = []
    for x in [[-1,0], [1, 0], [0,-1], [0, 1]]:
        a = np.add(loc, x)
        a = list(a)
        if not adaptive:
            if Utility.inRange(a, size) and currentMap[a[0], a[1]] != 1 and not any(a == x for x in closed) \
                    and not any(x.loc == a for x in openList):
                locs.append(a)
        else:
            if Utility.inRange(a, size) and currentMap[a[0], a[1]] != 1 and not any(x.loc == a for x in openList):
                locs.append(a)
    return locs

# while we have nodes to go to

# print path by starting at goal
def getPath(start, reverse, g, current):
    if reverse:
        start = goal
    cur = current
    if g:
        for c in closed:
            c.adaptive(g)
    pathL = [cur.loc]
    while cur.loc != start:
        cur = cur.parent
        pathL.append(cur.loc)
    if not reverse:
        pathL.reverse()
    return pathL


# finds a path using A*
def findPath(start, reverse=False, adaptive=False):
    if adaptive and reverse:
        print("Sorry, cannot do backwards adaptive!")
        return None
    g = 0 # used for adaptive
    global goal
    localGoal = goal
    if reverse:
        localGoal, start = start, localGoal # reverse the values for backwards
    global openList
    global closed
    if closed:
        if adaptive: # add nodes back with new values
            item = next((x for x in closed if x.loc == agent), 0)
            item.updateG() #
            openList = []
            hpq.heappush(item)
        else:
            openList = []
            hpq.heappush(openList, Utility.Node(start, hi=Utility.distance(start, localGoal)))
    else:
        hpq.heappush(openList, Utility.Node(start, gi=0, hi=Utility.distance(start, localGoal)))
    foundGoal = False
    current = None
    while openList and not foundGoal:
        current = hpq.heappop(openList) # get next best position
        closed.append(current.loc)  # add node to closed list

        if current.loc == localGoal: # found goal
            if adaptive:
                g = current.g # get final g
            foundGoal = True
            break

        global nodes
        nodes += 1

        possibleMoves = createPossible(current.loc)  # get list of all possible nodes
        for x in possibleMoves:
            # Node(location, parent, g, h)Utility.distance(start, localGoal)
            node = Utility.Node(x, current, current.g + 1, Utility.distance(x, localGoal))
            hpq.heappush(openList, node) # add it to binary heap

    if foundGoal:
        return getPath(start, reverse, g, current)
    else:
        return []


# move agent and remove fog of war
def moveAgent(path, adaptive=False):
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
            if not adaptive: # keep items in list for adaptive to refer back later
                closed = [path[y-1]] # get rid of unused items in closed list
            break

# main method
if __name__ == '__main__':
    adaptive = False
    start = [0, 0]
    goal = [size - 1, size - 1]
    agent = start
    updateMap(agent)  # remove fog of war
    while agent != goal:
        path = findPath(agent,adaptive=adaptive) # get path (need to create one for reverse)

        if path:    # if there is a path, move agent
            moveAgent(path, adaptive)
        else:   # no path, unable to get to goal
            finalPath = []
            print("No path found")
            break

    if finalPath:
        print("Final path = {}".format(finalPath))
    ui.gui(currentMap)

#