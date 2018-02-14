import heapq as hpq

import numpy as np

import Utility

# load in a test case
ACTUAL = np.load('test.npy')
# create blank board
currentMap = np.full((101, 101), 0, dtype=np.int8)
openList = []
hpq.heappush(openList, Utility.Node([0, 0], hi=Utility.distance([0, 0], [100, 100])))
closed = []  # always empty at start

# updates map before planning route
def updateMap(loc):
    for x in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        a = np.add(loc, x)
        a = list(a)
        if (Utility.inRange(a)):
            currentMap[a[0], a[1]] = ACTUAL[a[0], a[1]]

# expands each node around current and makes sure we haven't been
# there or isn't blocked
def createPossible(loc):
    locs = []
    for x in [[-1,0], [1, 0], [0,-1], [0, 1]]:
        a = np.add(loc, x)
        a = list(a)
        if Utility.inRange(a) and currentMap[a[0], a[1]] != 1 and not any(x.loc == a for x in closed):
            locs.append(a)
    return locs

# while we have nodes to go to

# print path by starting at goal
def getPath(start):
    cur = closed[-1]
    path = [cur.loc]
    while cur.loc != start:
        cur = cur.parent
        path.append(cur.loc)

# finds a path using a star
def findPath(start, goal):
    foundGoal = False
    while openList and not foundGoal:
        current = hpq.heappop(openList) # get next best position
        if current.loc == goal: # found goal
            foundGoal = True
            break
        updateMap(current.loc) # remove fog of war
        print(currentMap)
        closed.append(current) # add node to closed list
        possibleMoves = createPossible(current.loc)  # get list of all possible nodes
        for x in possibleMoves:
            x = list(x) # convert to list
            # Node(location, parent, g, h)
            node = Utility.Node(x, current, current.g + Utility.distance(current.loc, goal), Utility.distance(x, goal))
            hpq.heappush(openList, node) # add it to binary heap
    if(foundGoal):
        getPath()
    else:
        print("No path to goal!")

# main method
if __name__ == '__main__':
    findPath([0,0], [100,100])

# process = psutil.Process(os.getpid())
# print(process.memory_info().rss)