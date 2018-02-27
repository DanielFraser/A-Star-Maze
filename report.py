from datetime import datetime
from random import randrange as rd

import numpy as np

import Repeated as R
import ui

# will hold results for report

states = []
#states[4] = [[3,1], [100,100]]
# g values big vs small
def createStates():
    for x in range(50):
        y = "Mazes/maze{}.npy".format(str(x).zfill(2))
        start = [0,0]
        goal = [100,100]
        a = R.AStar(y, start, goal, adaptive=True)
        isPath = a[2]
        while not isPath:
            maps = np.load(y)
            start = [rd(0,10),rd(0,10)]
            while maps[start[0], start[1]] != 0:
                start = [rd(0, 10), rd(0, 10)]
            goal = [rd(75, 100), rd(75, 100)]
            while maps[goal[0], goal[1]] != 0:
                goal = [rd(0, 10), rd(0, 10)]
            a = R.AStar(y, start, goal, adaptive=True)
            isPath = a[2]
        states.append([start,goal])
        print(x)

def part2(start=0, end=0, times = 10, gui=False):
    smallg = []
    bigg = []
    for x in range(start, end): # goes through all 50 mazes
        start2 = datetime.now()
        state = [[0, 0], [100, 100]]
        ftemp = [0, datetime.now()]
        rtemp = [0, datetime.now()]
        for _ in range(times):
            y = "Mazes/maze{}.npy".format(str(x).zfill(2))
            a = R.AStar(y, state[0], state[1], smallG=False, gui=gui)
            ftemp[0] += a[0]
            ftemp[1] += a[1]
            b = R.AStar(y, state[0], state[1], smallG=True, gui=gui)
            rtemp[0] += b[0]
            rtemp[1] += b[1]
            bigg.append([round(ftemp[0] / 10), (ftemp[1] - start2) / 2])
        smallg.append([round(rtemp[0] / 10), (rtemp[1] - start2) / 2])
        print(y)
    print("small g vs big g")
    for i in range(0, end-start):
        print("{}: {} vs {}".format(i+start, smallg[i][0], bigg[i][0]))

# forward vs backward
def part3(start=0, end=50, times = 10, gui=False):
    forward = []
    reverse = []
    for x in range(start, end):  # goes through all 50 mazes
        start2 = datetime.now()
        state = [[0, 0], [100,100]]
        ftemp = [0, datetime.now()]
        rtemp = [0, datetime.now()]
        for _ in range(times): # so we get avg time
            y = "Mazes/maze{}.npy".format(str(x).zfill(2))
            a = R.AStar(y, state[0], state[1], reverse=False, gui=gui)
            ftemp[0] += a[0]
            ftemp[1] += a[1]
            b = R.AStar(y, state[0], state[1], reverse=True, gui=gui)
            rtemp[0] += b[0]
            rtemp[1] += b[1]

        forward.append([round(ftemp[0]/10), (ftemp[1] - start2)/2])
        reverse.append([round(rtemp[0] / 10), (rtemp[1] - start2) / 2])
        print(y)
    print("forward vs reverse")
    for i in range(0, end-start):
        print("{}: {} vs {}".format(i+start, forward[i][0], reverse[i][0]))


# forward vs adaptive
def part5(start=0, end=50, times = 10, gui=False):
    forward = []
    adaptive = []
    for x in range(start,end):  # goes through all 50 mazes
        y = "Mazes/maze{}.npy".format(str(x).zfill(2))
        start2 = datetime.now()
        state = [[0, 0], [100,100]]
        ftemp = [0, datetime.now()]
        rtemp = [0, datetime.now()]
        for _ in range(times):
            a = R.AStar(y, state[0], state[1], adaptive=False, gui=gui)
            ftemp[0] += a[0]
            ftemp[1] += a[1]
            b = R.AStar(y, state[0], state[1], adaptive=True, gui=gui)
            rtemp[0] += b[0]
            rtemp[1] += b[1]
        print(y)
        forward.append([round(ftemp[0] / 10), (ftemp[1] - start2) / 2])
        adaptive.append([round(rtemp[0] / 10), (rtemp[1] - start2) / 2])
    print("forward vs adaptive")
    for i in range(0, end-start):
        print("{}: {} vs {}".format(i+start, forward[i][0], adaptive[i][0]))

# prints every maze
def printMaze():
    for x in range(50):  # goes through all 50 mazes
        y = "Mazes/maze{}.npy".format(str(x).zfill(2))
        ui.gui(np.load(y), 101, [2,2],[100,100])
        input()

# show map of a certain maze
def showMap(num=0):
    y = "Mazes/maze{}.npy".format(str(num).zfill(2))
    ui.gui(np.load(y), 101, list(states[num][0]), list(states[num][1]), [])

# chooses a random maze for all 3
def demo():
    start = 4
    part2(start, start+1, 1, True)
    part3(start, start+1, 1, True)
    part5(start, start+1, 1, True)

if __name__ == '__main__':
    demo()