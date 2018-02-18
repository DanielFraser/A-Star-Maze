
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
        self.h += g
        self.f += g # difference between new and old f is g

    def __repr__(self):
        return "loc: {}, f: {}, g: {}".format(self.loc, self.f, self.g)

def distance(curPos, goal):
    return abs(curPos[0] - goal[0]) + abs(curPos[1] - goal[1])


def inRange(loc, size=100):
    return not (loc[0] < 0 or loc[0] > size - 1 or loc[1] < 0 or loc[1] > size - 1)