import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from utils.statusbar import Sequential, Stage

plt.style.use('ggplot')

divx = 2000
divy = 2000
lx = -2.0
ly = -2.0
rx = 2.0
ry = 2.0


class Limits:
    """
    todo: move all constraints here, make as a parameter to __main__
    """

    def __init__(self, **kwargs):
        for k, v in kwargs:
            self.__setattr__(k, v)


def squared_distance(z1: complex, z2: complex) -> float:
    """Squared distance between two complex numbers

    Same as abs((z1 - z2) ** 2)
    """
    return (z1.real - z2.real) ** 2 + (z1.imag - z2.imag) ** 2


class Plane:
    # roots of equation are 1, (-1-sqrt(3)i)/2 and (-1+sqrt(3)i)/2
    roots = [
        1.0 + 0.0j,
        -0.5 - math.sqrt(3.0) * 1.0j / 2.0,
        -0.5 + math.sqrt(3.0) * 1.0j / 2.0,
    ]
    eps = 1e-5
    Eps = 1e5

    @staticmethod
    def check(z: complex):
        """Positioning status of complex number

        :param z: complex number
        :returns:
            -1 if point is too far from all of the roots
            None if we still don't know which root is a limit of our iterative sequence
            <root number> otherwise
        """
        dists = [squared_distance(z, root) for root in Plane.roots]
        for i in range(0, len(dists)):
            if dists[i] < Plane.eps:
                return i
        for i in range(0, len(dists)):
            if dists[i] < Plane.Eps:
                return None
        return -1


def newton_iterations_alternative(z):
    """
    z_{j+1} = (2 / 3) * z_j + (1/3) * (1 / z_j^2)
    z_j = re + im * i
    z_{j+1} = (2 / 3) * z_j + (1/3) * (1 / (re^2 - im^2 + 2re * im * i))
    z_{j+1} = (2 / 3) * z_j + (1/3) * ((re^2 - im^2 - 2re * im * i) / ((re^2 - im^2)^2 + 4re^2 * im^2))
    z_{j+1} = (2 / 3) * z_j + (1/3) * ((re^2 - im^2 - 2re * im * i) / (re^2 + im^2)^2)
    z_{j+1} = (2 / 3) * re + (1/3) * (re^2 - im^2)/(re^2 + im^2)^2 +
    + (2/3) * (im - re * im / (re^2 + im^2)^2) * i

    :param z:
    :return:
    """
    pass


def newton_iterations(z):
    """Multiple iteration transition z_j -> z_{j+1}

    z_{j+1} = z_j - f(z_j) / f'(z_j)
        f(z) = z^3 - 1
        f'(z) = 3 * z^2
    z_{j+1} = z_j - (z_j^3 - 1) / (3 * z_j^2)
    z_{j+1} = (3 * z_j^3 - z_j^3 + 1) / (3 * z_j^2)
    z_{j+1} = (2 * z_j^3 + 1) / (3 * z_j^2)

    :param z: previous iteration value
    :return: positioning status of iteration limit
    """
    while Plane.check(z) is None:
        if z == 0.0:
            return -1
        z = (2 * (z ** 3) + 1) / (3 * (z ** 2))
        # denominator = ((z.re ** 2.0) + (z.im ** 2.0)) ** 2.0
        # if denominator == 0.0:
        #     return -1
        # new_re = (2.0 / 3.0) * z.re + (1.0 / 3.0) * ((z.re ** 2.0) - (z.im ** 2.0)) / denominator
        # new_im = (2.0 / 3.0) * (z.im - (z.re * z.im) / denominator)
        # z = Complex(new_re, new_im)
    return Plane.check(z)


def do():
    status = Sequential(
        Stage('Rows', divx + 1).every(divx // 100),
        Stage('Graph', 1)
    ).every(20)

    points = [[], [], [], []]
    print(status)
    for i in range(0, divx + 1):
        for j in range(0, divy + 1):
            z = complex(lx + i * (rx - lx) / divx, ly + j * (ry - ly) / divy)
            k = newton_iterations(z)
            points[k].append(z)
        status.step()

    plt.figure()
    for i in range(4):
        x = []
        y = []
        for v in points[i]:
            x.append(v.real)
            y.append(v.imag)
        if i == 0:
            plt.plot(x, y, 'o', color="red", markersize=100.0 * (rx - lx) / float(divx))
        if i == 1:
            plt.plot(x, y, 'o', color="green", markersize=100.0 * (rx - lx) / float(divx))
        if i == 2:
            plt.plot(x, y, 'o', color="blue", markersize=100.0 * (rx - lx) / float(divx))
        if i == 3:
            plt.plot(x, y, 'o', color="black", markersize=100.0 * (rx - lx) / float(divx))
    plt.savefig("./task3/out/graph.png")
    status.step()
    plt.show()
    # print(newton_iterations(Complex(-2.0, 2.0)))
