

class Node:
    # constructor that
    def __init__(self, loci, parenti=None, gi=1, hi=-1):
        self.loc = loci
        self.parent = parenti
        self.g = gi
        self.h = hi
        self.f = self.g + self.h

    # almost like equals method in java, but for less than (needed for binary heap)
    def __lt__(self, other):
        if self.f != other.f:
            return self.f < other.f
        else:
            return self.g > other.g


def distance(curPos, goal):
    return abs(curPos[0] - goal[0]) + abs(curPos[1] - goal[1])


def inRange(loc):
    return not (loc[0] < 0 or loc[0] > 100 or loc[1] < 0 or loc[1] > 100)




