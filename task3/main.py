import os
import math
import numpy as np
import colorsys
import matplotlib as mpl
import matplotlib.pyplot as plt

from typing import List, Callable, Union
from utils.statusbar import Stage, Iteration, Sequence
from utils.coloring import red_green_range, distinct_palette

plt.style.use('ggplot')


def squared_distance(z1: complex, z2: complex) -> float:
    """Squared distance between two complex numbers

    Same as abs((z1 - z2) ** 2)
    """
    return (z1.real - z2.real) ** 2 + (z1.imag - z2.imag) ** 2


class PictureEnv:
    def __init__(self, lx: int, ly: int, rx=None, ry=None, px=1000, py=1000, c=3):
        self.lx = lx
        self.rx = rx if rx is not None else abs(lx)
        self.ly = ly
        self.ry = ry if ry is not None else abs(ly)
        self.px = px
        self.py = py
        self.colors = distinct_palette(c)

    def width(self):
        return self.rx - self.lx

    def height(self):
        return self.ry - self.ly


class Plane:
    eps = 1e-5
    Eps = 1e5

    def __init__(self, roots: List[complex], *args: Callable[[complex], complex]):
        self.roots = roots
        self.transformers = args
        self.id = 0

    def select_transformer(self, tid: int):
        self.id = tid
        return self

    def transform(self, z):
        return self.transformers[self.id](z)

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
        self.status = None
        self.schedule = []

    def newton_iterations(self, z: complex) -> (List[complex], int):
        """Multiple iteration transition z -> lim z_j

        :param z: previous iteration value
        :return: positioning status of iteration limit
        """
        sequence = [z]
        while self.plane.check(z) is None:
            if z == 0.0:
                return sequence, -1
            z = self.plane.transform(z)
            sequence.append(z)
        return sequence, self.plane.check(z)

    def sequence(self, z, limits: PictureEnv, filename: str):
        self.schedule.append((
            self.__save_sequence,
            {
                'zs': np.array([z] if isinstance(z, complex) else z),
                'limits': limits,
                'filename': filename
            }
        ))
        return self

    def classification(self, limits: PictureEnv, filename: str):
        self.schedule.append((
            self.__save_classification,
            {'limits': limits, 'filename': filename, }
        ))
        return self

    def __status(self, stage):
        if stage[0] == self.__save_sequence:
            zs = stage[1]["zs"]
            line = str(zs)
            if len(line) > 10:
                line = line[:10] + '...'
            return Sequence(
                f'Sequence {line}',
                Stage('Calculating', len(zs)),
                Stage('Saving', 1)
            )
        elif stage[0] == self.__save_classification:
            limits = stage[1]['limits']
            return Sequence(
                f'Classification [{limits.lx}:{limits.rx}]x[{limits.ly}:{limits.ry}]',
                Stage('Calculating', limits.width() * limits.px + 1),
                Stage('Saving', 1)
            )

    def run(self):
        stages = list(map(self.__status, self.schedule))
        self.status = Sequence('All', *stages).width(50)
        self.status.__getattribute__('_cached_print')()
        for s in self.schedule:
            s[0](**s[1])
        self.status = None

    def __save_sequence(self, zs, limits: PictureEnv, filename: str):
        plt.figure()
        plt.axis('equal')
        plt.xlim(limits.lx, limits.rx)
        plt.ylim(limits.ly, limits.ry)

        for z in zs:
            s, k = self.newton_iterations(z)
            x = [zz.real for zz in s]
            y = [zz.imag for zz in s]
            root = self.plane.roots[k]

            plt.scatter(x, y, s=np.linspace(50, 10, len(s)), c=red_green_range(len(s)))
            plt.plot(x, y, 'o', color='black', lw=1, ls='-', ms=1)
            plt.plot(root.real, root.imag, 'gh', ms=7)
            if self.status is not None:
                self.status.step()

        plt.savefig(os.path.join(os.getcwd(), 'task3', 'out', f'{filename}.png'))
        if self.status is not None:
            self.status.step()

    def __save_classification(self, limits: PictureEnv, filename: str):
        w, h = limits.width() * limits.px + 1, limits.height() * limits.py + 1
        roots = len(self.plane.roots)
        points = [[] for _ in range(roots + 1)]
        for i in range(0, w):
            for j in range(0, h):
                z = complex(limits.lx + limits.width() * i / w, limits.ly + limits.height() * j / h)
                _, k = self.newton_iterations(z)
                points[k].append(z)
            if self.status is not None:
                self.status.step()

        plt.figure()
        plt.axis('equal')
        for i in range(roots + 1):
            x = [z.real for z in points[i]]
            y = [z.imag for z in points[i]]
            plt.plot(x, y, 'o', color=limits.colors[i], ms=1)
        plt.savefig(os.path.join(os.getcwd(), 'task3', 'out', f'{filename}.png'))

        if self.status is not None:
            self.status.step()
