from datetime import datetime

import Repeated as R


# will hold results for report
# TODO multithreading? (can't do much)
# g values big vs small
states = dict() # will hold special start and end goals for certain mazes
states[0] = [[0,0],[100,100]]

def part2():
    smallg = []
    bigg = []
    for x in range(2): # goes through all 50 mazes
        ftemp = [0, datetime.now()]
        rtemp = [0, datetime.now()]
        state = [[0,0],[100,100]]
        if x in states:
            state = states[x]
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

# forward vs backward
def part3():
    forward = []
    reverse = []
    # start = 0
    for x in range(1):  # goes through all 50 mazes
        state = [[0, 0], [100, 100]]
        if x in states:
            state = states[x]
        ftemp = [0,datetime.now()]
        rtemp = [0,datetime.now()]
        for z in range(10): # so we get avg time
            y = "Mazes/maze{}.npy".format(str(x).zfill(2))
            a = R.AStar(y, state[0], state[1], reverse=False)
            ftemp[0] += a[0]
            ftemp[1] += a[1]
            b = R.AStar(y, state[0], state[1], reverse=True)
            rtemp[0] += b[0]
            rtemp[1] += b[1]
            print(z)
        forward.append(ftemp[0]/10)
        forward.append(ftemp[1])
        reverse.append(rtemp[0]/10)
        reverse.append(rtemp[1])
        print(y)

# forward vs adaptive
def part5():
    forward = []
    adaptive = []
    for x in range(50):  # goes through all 50 mazes
        ftemp = [0, datetime.now()]
        rtemp = [0, datetime.now()]
        state = [[0, 0], [100, 100]]
        if x in states:
            state = states[x]
        for _ in range(10):
            y = "Mazes/maze{}.npy".format(str(x).zfill(2))
            a = R.AStar(y, state[0], state[1], adaptive=False)
            ftemp[0] += a[0]
            ftemp[1] += a[1]
            b = R.AStar(y, state[0], state[1], adaptive=True)
            rtemp[0] += b[0]
            rtemp[1] += b[1]
        print(y)
    forward.append(ftemp[0] / 10)
    forward.append(ftemp[1])
    adaptive.append(rtemp[0] / 10)
    adaptive.append(rtemp[1])
    # print(forward[1][1])
    # print(adaptive[1][1])


if __name__ == '__main__':
    # part2()
    # part3()
    part5()
