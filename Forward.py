import heapq as hpq

import numpy as np

import Utility

size = 101
# load in a test case
ACTUAL = np.load('Mazes/maze01.npy')
#print(ACTUAL)
#ACTUAL = np.full((size, size), 0, dtype=np.int8)
#ACTUAL[2,0] = 1
#ACTUAL[18,19] = 1
#ACTUAL[19,18] = 1
# create blank board
currentMap = np.full((size, size), 0, dtype=np.int8)
openList = []
closed = []  # always empty at start
finalPath = []

# updates map before planning route
def updateMap(loc):
    for x in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        a = np.add(loc, x)
        a = list(a)
        if (Utility.inRange(a, size)):
            currentMap[a[0], a[1]] = ACTUAL[a[0], a[1]]

# expands each node around current and makes sure we haven't been
# there or isn't blocked
def createPossible(loc):
    locs = []
    for x in [[-1,0], [1, 0], [0,-1], [0, 1]]:
        a = np.add(loc, x)
        a = list(a)
        if Utility.inRange(a, size) and currentMap[a[0], a[1]] != 1 and not any(x.loc == a for x in closed):
            locs.append(a)
    return locs

# while we have nodes to go to

# print path by starting at goal
def getPath(start, reverse):
    if reverse:
        start = goal
    cur = closed[-1]
    pathL = [cur]
    while cur.loc != start:
        cur = cur.parent
        pathL.append(cur)
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
    if closed:
        openList = []
        closed[-1].g = 0
        closed[-1].f = closed[-1].g + Utility.distance(closed[-1].loc, localGoal)
        hpq.heappush(openList, closed[-1])
    else:
        hpq.heappush(openList, Utility.Node(start, gi=0, hi=Utility.distance(start, localGoal)))
    foundGoal = False
    while openList and not foundGoal:
        current = hpq.heappop(openList) # get next best position
        closed.append(current)  # add node to closed list

        if current.loc == localGoal: # found goal
            foundGoal = True
            break

        possibleMoves = createPossible(current.loc)  # get list of all possible nodes
        for x in possibleMoves:
            # Node(location, parent, g, h)Utility.distance(start, localGoal)
            node = Utility.Node(x, current, current.g + 1, Utility.distance(x, localGoal))
            hpq.heappush(openList, node) # add it to binary heap

    if foundGoal:
        return getPath(start, reverse)
    else:
        return []

# move agent and remove fog of war
def moveAgent(path):
    for y,x in enumerate(path):
        x = x.loc
        global finalPath
        if currentMap[x[0], x[1]] == 0:
            updateMap(x)  # remove fog of war
            global agent
            agent = x
            finalPath.append(x)
        else:
            finalPath = finalPath[:-1]
            global closed
            closed = [path[y-1]] # get rid of unused items in closed list
            break

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

# need backtracking and updating g values