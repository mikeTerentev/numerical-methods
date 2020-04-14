import os
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from typing import List
from utils.statusbar import Stage, Iteration, Sequence

plt.style.use('ggplot')


def squared_distance(z1: complex, z2: complex) -> float:
    """Squared distance between two complex numbers

    Same as abs((z1 - z2) ** 2)
    """
    return (z1.real - z2.real) ** 2 + (z1.imag - z2.imag) ** 2


class PictureEnv:
    colors = ['red', 'green', 'blue', 'black']

    def __init__(self, lx: int, ly: int, rx=None, ry=None, px=1000, py=1000):
        self.lx = lx
        self.rx = rx if rx is not None else abs(lx)
        self.ly = ly
        self.ry = ry if ry is not None else abs(ly)
        self.px = px
        self.py = py

    def width(self):
        return self.rx - self.lx

    def height(self):
        return self.ry - self.ly


class Plane:
    eps = 1e-5
    Eps = 1e5

    def __init__(self, roots):
        self.roots = roots

    def check(self, z: complex):
        """Positioning status of complex number

        :param z: complex number
        :returns:
            -1 if point is too far from all of the roots
            None if we still don't know which root is a limit of our iterative sequence
            <root number> otherwise
        """
        dists = [squared_distance(z, root) for root in self.roots]
        for i in range(0, len(dists)):
            if dists[i] < Plane.eps:
                return i
        for i in range(0, len(dists)):
            if dists[i] < Plane.Eps:
                return None
        return -1


class NewtonIterator:
    def __init__(self, plane: Plane):
        self.plane = plane

    def newton_iterations(self, z: complex) -> (List[complex], int):
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
        sequence = [z]
        while self.plane.check(z) is None:
            if z == 0.0:
                return sequence, -1
            z = (2 * (z ** 3) + 1) / (3 * (z ** 2))
            sequence.append(z)
        return sequence, self.plane.check(z)

    def newton_iterations_alternative(self, z: complex) -> (List[complex], int):
        """Multiple iteration transition (in real/imag form)

        z_{j+1} = (2 / 3) * z_j + (1 / 3) * (1 / z_j^2)
            z_j = re + im * i
        z_{j+1} = (2 / 3) * z_j + (1 / 3) * (1 / (re^2 - im^2 + 2 re * im * i))
        z_{j+1} = (2 / 3) * z_j + (1 / 3) * ((re^2 - im^2 - 2 re * im * i) / ((re^2 - im^2)^2 + 4 re^2 * im^2))
        z_{j+1} = (2 / 3) * z_j + (1 / 3) * ((re^2 - im^2 - 2 re * im * i) / (re^2 + im^2)^2)
        z_{j+1} = (2 / 3) * re + (1 / 3) * (re^2 - im^2) / (re^2 + im^2)^2 +
                + (2 / 3) * (im - re * im / (re^2 + im^2)^2) * i

        :param z: previous iteration value
        :return: positioning status of iteration limit
        """
        sequence = [z]
        while self.plane.check(z) is None:
            denominator = ((z.real ** 2.0) + (z.imag ** 2.0)) ** 2.0
            if denominator == 0.0:
                return sequence, -1
            new_re = (2.0 / 3.0) * z.real + (1.0 / 3.0) * ((z.real ** 2.0) - (z.imag ** 2.0)) / denominator
            new_im = (2.0 / 3.0) * (z.imag - (z.real * z.imag) / denominator)
            z = complex(new_re, new_im)
            sequence.append(z)
        return sequence, self.plane.check(z)

    def save_sequence(self, z: complex, filename: str):
        s, k = self.newton_iterations(z)
        x = [zz.real for zz in s]
        y = [zz.imag for zz in s]
        size = max(1, max(max(x) - min(x), max(y) - min(y)) / 2 / len(s))
        root = self.plane.roots[k]

        plt.figure()
        plt.plot(x, y, 'o', color='black', markersize=size, scalex=1, scaley=1)
        plt.plot(z.real, z.imag, 'o', color='red', markersize=size + 1, scalex=1, scaley=1)
        plt.plot(root.real, root.imag, 'o', color='blue', markersize=size + 1, scalex=1, scaley=1)
        plt.savefig(os.path.join(os.getcwd(), 'task3', 'out', filename))

    def save_classification(self, limits: PictureEnv, filename: str, verbose=True):
        w, h = limits.width() * limits.px + 1, limits.height() * limits.py + 1
        status = None
        roots = len(self.plane.roots)

        if verbose:
            status = Sequence(
                Stage('Calculating', w),
                Stage('Saving', 1)
            ).width(50)
            print(status)

        points = [[] for _ in range(roots + 1)]
        for i in range(0, w):
            for j in range(0, h):
                z = complex(limits.lx + limits.width() * i / w, limits.ly + limits.height() * j / h)
                _, k = self.newton_iterations(z)
                points[k].append(z)
            if verbose:
                status.step()

        plt.figure()
        for i in range(roots + 1):
            x = [z.real for z in points[i]]
            y = [z.imag for z in points[i]]
            plt.plot(x, y, 'o', color=limits.colors[i], markersize=1, scalex=1, scaley=1)
        plt.savefig(os.path.join(os.getcwd(), 'task3', 'out', filename))
        if verbose:
            status.step()
