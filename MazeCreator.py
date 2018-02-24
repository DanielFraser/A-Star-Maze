import numpy as np

def a():
    for x in range(50):
        a = np.random.choice(a=[0,  1], size=(101, 101), p=[7/10, 3/10])
        a[0, 0] = 0
        a[100,100] = 0
        name = str(x).zfill(2)
        name = 'Mazes/maze'+name
        np.save(name, a)