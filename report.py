from datetime import datetime

import Repeated as R


# will hold results for report
# TODO fix bug where variables don't reset their values when run past first time
# TODO add a 2nd for loop inside the maze loops to get avg times for both cases
# TODO multithreading?
# g values big vs small


def part2():
    smallg = []
    bigg = []
    for x in range(2): # goes through all 50 mazes
        for _ in range(10):
            y = "Mazes/maze{}.npy".format(str(x).zfill(2))
            a = R.AStar(y, [0, 0], [100, 100], smallG=False)
            bigg.append(a)
            b = R.AStar(y, [0, 0], [100, 100], smallG=True)
            smallg.append(b)
        print(y)

# forward vs backward
def part3():
    forward = []
    reverse = []
    start = 0
    for x in range(1):  # goes through all 50 mazes
        start = datetime.now()
        ftemp = [0,datetime.now()]
        rtemp = [0,datetime.now()]
        for z in range(10): # so we get avg time
            y = "Mazes/maze{}.npy".format(str(x).zfill(2))
            a = R.AStar(y, [0, 0], [100, 100], reverse=False)
            ftemp[0] += a[0]
            ftemp[1] += a[1]
            b = R.AStar(y, [0, 0], [100, 100], reverse=True)
            rtemp[0] += b[0]
            rtemp[1] += b[1]
            print(z)
        forward.append(ftemp[0]/10)
        forward.append(ftemp[1])
        reverse.append(rtemp[0]/10)
        reverse.append(rtemp[1])
        print(y)
    print(forward)
    print(reverse)
    print("forward: avg nodes = {}, avg time = {}".format(forward[0], (forward[1] - start)/2))
    print("backward: avg nodes = {}, avg time = {}".format(reverse[0], (reverse[1] - start)/2))

# forward vs adaptive
def part5():
    forward = []
    adaptive = []
    for x in range(50):  # goes through all 50 mazes
        for _ in range(10):
            y = "Mazes/maze{}.npy".format(str(x).zfill(2))
            a = R.AStar(y, [0, 0], [100, 100], adaptive=False)
            forward.append(a)
            b = R.AStar(y, [0, 0], [100, 100], adaptive=True)
            adaptive.append(b)
        print(y)
    # print(forward[1][1])
    # print(adaptive[1][1])


if __name__ == '__main__':
    # part2()
    part3()
    # part5()