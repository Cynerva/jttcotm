import random


def heightmap_1d(iterations, seed=None, mul=0.5):
    """ Midpoint displacement! """
    if seed != None:
        random.seed(seed)

    heightmap = [0.0]

    multiplier = 1.0
    for _ in range(iterations):
        old_size = len(heightmap)

        new_heights = []
        for i in range(old_size):
            left = heightmap[i]
            right = heightmap[(i + 1) % old_size]
            mid = (left + right) / 2.0 + random.uniform(-1.0, 1.0)*multiplier
            new_heights += [left, mid]
        heightmap = new_heights

        multiplier *= mul

    start_index = random.randint(0, len(heightmap) - 1)
    heightmap = heightmap[start_index:] + heightmap[:start_index]

    return heightmap
