import Repeated as R
# will hold results for report
# TODO fix bug where variables don't reset their values when run past first time
# g values big vs small


def part2():
    smallg = []
    bigg = []
    for x in range(50): # goes through all 50 mazes
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
    for x in range(50):  # goes through all 50 mazes
        y = "Mazes/maze{}.npy".format(str(x).zfill(2))
        a = R.AStar(y, [0, 0], [100, 100], reverse=False)
        forward.append(a)
        b = R.AStar(y, [0, 0], [100, 100], reverse=True)
        reverse.append(b)
        print(y)


# forward vs adaptive
def part5():
    forward = []
    adaptive = []
    for x in range(50):  # goes through all 50 mazes
        y = "Mazes/maze{}.npy".format(str(x).zfill(2))
        a = R.AStar(y, [0, 0], [100, 100], adaptive=False)
        forward.append(a)
        b = R.AStar(y, [0, 0], [100, 100], adaptive=True)
        adaptive.append(b)
        print(y) # so we know which maze


if __name__ == '__main__':
    part2()
    part3()
    part5()