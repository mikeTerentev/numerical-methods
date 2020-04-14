import math
from task3.main import NewtonIterator, Plane, PictureEnv


def task1():
    # todo
    pass


def task2():
    # todo
    pass


def task3():
    ni = NewtonIterator(Plane([
        1.0 + 0.0j,
        -0.5 - math.sqrt(3.0) * 1.0j / 2.0,
        -0.5 + math.sqrt(3.0) * 1.0j / 2.0,
    ]))
    for i, z in enumerate([1.0 + 0.75j, -1 - 0.5j, 1.5 + 0.5j]):
        ni.save_sequence(z, f'sequence-{i}.png')
    ni.save_classification(
        PictureEnv(lx=-2, ly=-2, px=500, py=500),
        'classification.png'
    )


if __name__ == '__main__':
    task1()
    task2()
    task3()
