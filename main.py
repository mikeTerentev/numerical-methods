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
        # z_{j+1} = z_j - f(z_j) / f'(z_j)
        #   f(z) = z^3 - 1
        #   f'(z) = 3 * z^2
        # z_{j+1} = z_j - (z_j^3 - 1) / (3 * z_j^2)
        # z_{j+1} = (3 * z_j^3 - z_j^3 + 1) / (3 * z_j^2)
        # z_{j+1} = (2 * z_j^3 + 1) / (3 * z_j^2)
        lambda z: (2 * (z ** 3) + 1) / (3 * (z ** 2)),
        # z_{j+1} = (2 / 3) * z_j + (1 / 3) * (1 / z_j^2)
        #   z_j = re + im * i
        # z_{j+1} = (2 / 3) * z_j + (1 / 3) * (1 / (re^2 - im^2 + 2 re * im * i))
        # z_{j+1} = (2 / 3) * z_j + (1 / 3) * ((re^2 - im^2 - 2 re * im * i) / ((re^2 - im^2)^2 + 4 re^2 * im^2))
        # z_{j+1} = (2 / 3) * z_j + (1 / 3) * ((re^2 - im^2 - 2 re * im * i) / (re^2 + im^2)^2)
        # z_{j+1} = (2 / 3) * re + (1 / 3) * (re^2 - im^2) / (re^2 + im^2)^2 +
        #         + (2 / 3) * (im - re * im / (re^2 + im^2)^2) * i
        lambda z: complex(
            (2.0 / 3.0) * z.real + (1.0 / 3.0) * ((z.real ** 2.0) - (z.imag ** 2.0)),
            (2.0 / 3.0) * (z.imag - (z.real * z.imag))
        ) / (((z.real ** 2.0) + (z.imag ** 2.0)) ** 2.0)
    ).select_transformer(0))

    limits = PictureEnv(lx=-2, ly=-2, px=500, py=500, c=4)
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
        'classification'
    ).run()


if __name__ == '__main__':
    task1()
    task2()
    task3()
