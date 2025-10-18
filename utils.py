from builtins import *


def max_dict(d):
    max_val = None
    max_key = None
    for key in d:
        val = d[key]
        if max_val == None or max_val < val:
            max_val = val
            max_key = key
    return max_key, max_val


def min_dict(d):
    min_val = None
    min_key = None
    for key in d:
        val = d[key]
        if min_val == None or min_val > val:
            min_val = val
            min_key = key
    return min_key, min_val


def random_direction():
    dirs = [North, East, South, West]
    index = random() * len(dirs) // 1
    return dirs[index]


def clamp_pos(pos):
    x, y = pos
    size = get_world_size()
    clamp_x = max(min(size - 1, x), 0)
    clamp_y = max(min(size - 1, y), 0)
    return (clamp_x, clamp_y)


def sign(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def log2(n):
    # Fake log2 implementation for n < 32
    if n < 1:
        raise ValueError("log2 undefined for n < 1")
    for i in range(32):
        if 2**i > n:
            return i - 1
        if 2**i == n:
            return i
    raise ValueError("n >= 32 not supported")
