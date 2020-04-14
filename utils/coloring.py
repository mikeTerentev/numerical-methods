import numpy as np
import colorsys


def red_green_range(size: int):
    r = np.linspace(1, 0, size)
    g = np.linspace(0, 1, size)
    return np.array([[r[i], g[i], 0] for i in range(size)])


def distinct_palette(size: int):
    hsv = [[(i / size), 0.5, 0.5] for i in range(size)]
    return np.array(list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv)))
