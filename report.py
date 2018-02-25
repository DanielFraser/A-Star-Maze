from datetime import datetime
import ui
import Repeated as R
import numpy as np
import sys
import Utility as u
from random import randrange as rd

# will hold results for report
# TODO multithreading? (can't do much)

states = []
#states[4] = [[3,1], [100,100]]
# g values big vs small
def createStates():
    for x in range(50):
        isPath = False
        while not isPath:
            y = "Mazes/maze{}.npy".format(str(x).zfill(2))
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

def part2():
    smallg = []
    bigg = []
    for x in range(2): # goes through all 50 mazes
        ftemp = [0, datetime.now()]
        rtemp = [0, datetime.now()]
        state = states[x]
        state = list(state)
        state[0] = list(state[0])
        state[1] = list(state[1])
        for _ in range(10):
            y = "Mazes/maze{}.npy".format(str(x).zfill(2))
            a = R.AStar(y, state[0], state[1], smallG=False)
            ftemp[0] += a[0]
            ftemp[1] += a[1]
            b = R.AStar(y, state[0], state[1], smallG=True)
            rtemp[0] += b[0]
            rtemp[1] += b[1]
        smallg.append(ftemp[0] / 10)
        smallg.append(ftemp[1])
        bigg.append(rtemp[0] / 10)
        bigg.append(rtemp[1])
        print(y)
    print(smallg)
    print(bigg)

# forward vs backward
def part3():
    forward = []
    reverse = []
    for x in range(2):  # goes through all 50 mazes
        start = datetime.now()
        state = states[x]
        state = list(state)
        state[0] = list(state[0])
        state[1] = list(state[1])
        ftemp = [0, datetime.now()]
        rtemp = [0, datetime.now()]
        for _ in range(10): # so we get avg time
            y = "Mazes/maze{}.npy".format(str(x).zfill(2))
            a = R.AStar(y, state[0], state[1], reverse=False)
            ftemp[0] += a[0]
            ftemp[1] += a[1]
            b = R.AStar(y, state[0], state[1], reverse=True)
            rtemp[0] += b[0]
            rtemp[1] += b[1]
            print('b')

        forward.append([round(ftemp[0]/10), (ftemp[1] - start)/2])
        reverse.append([round(rtemp[0] / 10), (rtemp[1] - start) / 2])
        print(y)
    print(forward)
    print(reverse)


# forward vs adaptive
def part5(end=50, start=0):
    forward = []
    adaptive = []
    for x in range(start,end):  # goes through all 50 mazes
        y = "Mazes/maze{}.npy".format(str(x).zfill(2))
        start = datetime.now()
        state = states[x]
        state = list(state)
        state[0] = list(state[0])
        state[1] = list(state[1])
        ftemp = [0, datetime.now()]
        rtemp = [0, datetime.now()]
        for _ in range(10):
            a = R.AStar(y, state[0], state[1], adaptive=False)
            ftemp[0] += a[0]
            ftemp[1] += a[1]
            b = R.AStar(y, state[0], state[1], adaptive=True)
            rtemp[0] += b[0]
            rtemp[1] += b[1]
            print('b')
        print(y)
        forward.append([round(ftemp[0] / 10), (ftemp[1] - start) / 2])
        adaptive.append([round(rtemp[0] / 10), (rtemp[1] - start) / 2])
    print("{} vs {}".format(forward[0][0], adaptive[0][0]))
    print("{} vs {}".format(forward[1][0], adaptive[1][0]))

def printMaze():
    for x in range(50):  # goes through all 50 mazes
        y = "Mazes/maze{}.npy".format(str(x).zfill(2))
        ui.gui(np.load(y), 101, [2,2],[100,100])
        input()

def testforpath(num=0):
    y = "Mazes/maze{}.npy".format(str(num).zfill(2))
    state = states[num]
    a = R.AStar(y, state[0], state[1], adaptive=True)
    print(a)
    ui.gui(np.load(y), 101, state[0], state[1], a[3])

if __name__ == '__main__':
    createStates()
    np.save('works', states)
    # a = np.load('works.npy')
    # states = a
    # print(a)
    # printMaze()
    # part2()
    # part3()
    # part5(2)
    #testforpath(0)
    #mc.redoMaze(4)