import numpy as np
import math, random
import matplotlib.pyplot as pyplot

def draw():
    xs = np.asarray(np.linspace(-15, 15, 5000)) #genplot
    #xs = np.asarray(np.linspace(6, 8, 5000)) #rightmost_root
    ys = [polynom(x) for x in xs]
    pyplot.plot(xs, ys)
    pyplot.xlabel('x')
    pyplot.ylabel('p(x)')
    pyplot.axvline(color='r')
    pyplot.axhline(color='r')
    axes = pyplot.gca()
    axes.set_ylim([-20, 20]) #y_resized
    #pyplot.vlines([6.7, 6.9], -20, 20, label='border') #rightmost_root, localization = [6.7, 6.9]
    #pyplot.vlines([-2.0, -1.6, -1.0, -0.6], -1, 1, label='border') #left_roots, localizations = [-1.8, -1.6, -1.0, -0.8]
    pyplot.show()


def calcentry(x, it):
    tangent = np.poly1d([1, -x]) * deriv(x) + polynom(x)
    print(tangent)
    root = np.asarray(tangent.r)
    assert(len(root) == 1)
    assert(abs(tangent(x) - polynom(x)) < eps)
    return [root[0], 0, x, tangent(x), x, it]

def newton(l, r):
    xs = [random.uniform(l, r)]
    while len(xs) < 2 or abs(xs[-1] - xs[-2]) > eps:
        xn = xs[-1]
        xs.append(xn - polynom(xn) / deriv(xn))
    #return xs
    ret = [calcentry(xs[i], i) for i in range(len(xs))]
    return ret


#x^7 - 5x^6 - 12x^5 + sqrt(2) x^2 - 4 = 0

polynom = np.poly1d([1, -5, -12, 0, 0, math.sqrt(2), 0, -4])
deriv = np.poly1d.deriv(polynom)
eps = 1e-6

#draw()

newton(6.7, 6.9)
#print(newton(6.7, 6.9))
