import math
import numpy as np

from task3.main import NewtonIterator, Plane, PictureEnv


def random(low, high, size):
    return low + np.random.random(size) * (high - low)


def task1():
    # todo
    pass


def task2():
    # todo
    pass


def task3():
    ni = NewtonIterator(Plane(
        [
            1.0 + 0.0j,
            -0.5 - math.sqrt(3.0) * 1.0j / 2.0,
            -0.5 + math.sqrt(3.0) * 1.0j / 2.0,
        ],
        lambda z: (2 * (z ** 3) + 1) / (3 * (z ** 2)),
        lambda z: z * 2 / 3 + complex(
            (z.real ** 2.0) - (z.imag ** 2.0),
            - 2 * z.real * z.imag
        ) / (3 * ((z.real ** 2.0) + (z.imag ** 2.0)) ** 2.0)
    ).select_transformer(1))

    limits = PictureEnv(lx=-2, ly=-2, px=1000, py=1000, c=4)
    ni.sequence(
        [1.0 + 0.75j, -1 - 0.5j, 1.5 + 0.5j],
        limits,
        'sequence'
    ).sequence(
        random(limits.lx, limits.rx, 30) + 1j * random(limits.ly, limits.ry, 30),
        limits,
        'random-sequence'
    ).classification(
        limits,
        'classification-other'
    ).run()


if __name__ == '__main__':
    task1()
    task2()
    task3()
