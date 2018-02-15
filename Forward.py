import heapq as hpq

import numpy as np

import Utility

size = 20
# load in a test case
#ACTUAL = np.load('test.npy')
ACTUAL = np.full((size, size), 0, dtype=np.int8)
# create blank board
currentMap = np.full((size, size), 0, dtype=np.int8)
agent = [0, 0]
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
    openList = []
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
    for x in path:
        x = list(x)
        updateMap(x) # remove fog of war
        if currentMap[x[0], x[1]] == 0:
            global agent
            agent = x
        else:
            return None # we need to find a new path


# main method
if __name__ == '__main__':
    start = [0, 0]
    goal = [size - 1, size - 1]
    agent = start
    updateMap(agent)  # remove fog of war
    while agent != goal:
        path = findPath(agent, True) # get path (need to create one for reverse)
        finalPath = path
        if path:    # if there is a path, move agent
            moveAgent(path)
        else:   # no path, unable to get to goal
            print("No path found")
            break
    print(finalPath)

# process = psutil.Process(os.getpid())
# print(process.memory_info().rss)