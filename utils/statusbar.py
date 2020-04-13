from abc import ABC, abstractclassmethod
from typing import Union, List
from os import system, name
from copy import deepcopy
from time import sleep
from sys import argv


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def indent(lines: str) -> str:
    return '\n'.join(map(lambda line: f'\t{line}', lines.split('\n')))


class Reportable:
    __width = 100
    __item = '-'

    def __init__(self, limit: int):
        self.all_ticks = 0
        self.ticks = 0
        self.limit = limit
        self.__every = 1
        self.__cache = ''

    def __ensure(self, ticks, limit):
        if ticks is None:
            ticks = self.ticks
        if limit is None:
            limit = self.limit
        return ticks, limit

    def _bar(self, ticks=None, limit=None) -> str:
        ticks, limit = self.__ensure(ticks, limit)
        ratio = ticks / limit
        items = int(self.__width * ratio)
        empty = '' if ratio == 1 else f'>{" " * (self.__width - items - 1)}'
        return f'[{self.__item * items}{empty}] {self._percent(ticks, limit)}'

    def _percent(self, ticks=None, limit=None) -> str:
        ticks, limit = self.__ensure(ticks, limit)
        return f'{100 * ticks // limit}%'

    def _ratio(self, ticks=None, limit=None) -> str:
        ticks, limit = self.__ensure(ticks, limit)
        return f'{ticks}/{limit}'

    def tick(self) -> bool:
        if self.ticks < self.limit:
            self.all_ticks += 1
            self.ticks += 1
            return True
        return False

    def _cached_print(self):
        out = self.__repr__()
        if out != self.__cache and self.all_ticks % self.__every == 0:
            self.__cache = out
            clear()
            print(out)

    def step(self):
        if self.tick():
            self._cached_print()

    def width(self, width: int):
        Reportable.__width = width
        return self

    def every(self, num: int):
        Reportable.__every = num
        return self

    def full_limit(self):
        return self.limit


class Stage(Reportable):
    def __init__(self, name: str, limit: int):
        super().__init__(limit)
        self.name = name

    def __repr__(self) -> str:
        return f'{self.name}:\n{self._bar()}\n'


class Iterations(Reportable):
    def __init__(self, limit: int, rep: Reportable):
        super().__init__(limit)
        self.ticks += 1
        self.origin = rep
        self.rep = deepcopy(self.origin)

    def tick(self) -> bool:
        if self.rep.tick():
            self.all_ticks += 1
            return True
        if self.ticks < self.limit:
            self.ticks += 1
            self.rep = deepcopy(self.origin)
            return self.tick()
        return False

    def full_limit(self):
        return self.limit * self.rep.full_limit()

    def __repr__(self):
        return f'Iteration {self._ratio()}:\n{self.rep}'


class Sequential(Reportable):
    def __init__(self, *args: Reportable):
        super().__init__(len(args) - 1)
        self.stages = args
        self.all_ticks = 0
        self.all_limit = self.full_limit()

    def __stage(self):
        return self.stages[self.ticks]

    def tick(self) -> bool:
        if self.__stage().tick():
            self.all_ticks += 1
            return True
        if self.ticks < self.limit:
            self.ticks += 1
            return self.tick()
        return False

    def full_limit(self):
        return sum([s.full_limit() for s in self.stages])

    def __repr__(self):
        return f'Progress (step {self._ratio(self.ticks + 1, self.limit + 1)}):\n' \
               f'{self._bar(self.all_ticks, self.all_limit)}\n' + \
               indent(''.join(map(str, self.stages[:self.ticks + 1])))


if __name__ == '__main__':
    status = Sequential(
        Stage("Singleton", 1),
        Stage("Stage 1", 400),
        Iterations(
            3,
            Sequential(
                Stage("Stage 2", 200),
                Stage("Stage 3", 300)
            )
        )
    ).every(10).width(50)

    status.__getattribute__('_cached_print')()
    wait = 0.001
    if len(argv) > 1 and argv[1] == '--debug':
        wait = 0.1
    while True:
        status.step()
        sleep(wait)
