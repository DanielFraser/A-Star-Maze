import Forward as f

class Node:
    # constructor
    def __init__(self, loci, parent=None, gi=1, hi=-1, smallG = False):
        self.loc = loci
        self.parent = parent
        self.g = gi
        self.f = self.g + hi
        self.h = hi
        self.bool = smallG

    # almost like equals method in java, but for less than (needed for binary heap)
    def __lt__(self, other):
        if self.f != other.f:
            return self.f < other.f
        else:
            if not self.bool:
                return self.g > other.g
            else:
                return self.g < other.g

    def adaptive(self, g):
        self.h = g - self.g
        self.f = self.g + self.h # difference between new and old f is g

    def updateG(self, g=0):
        self.g = g
        self.f = self.g + self.h

    def __repr__(self):
        return "loc: {}, f: {}, g: {}".format(self.loc, self.f, self.g)

def distance(curPos, goal):
    item = next((x for x in f.closed if x.loc == curPos), 0)
    if item: # get distance from last time and remove it from closed
        f.closed.remove(item)
        return item.h
    else:
        return abs(curPos[0] - goal[0]) + abs(curPos[1] - goal[1])


def inRange(loc, size=100):
    return not (loc[0] < 0 or loc[0] > size - 1 or loc[1] < 0 or loc[1] > size - 1)