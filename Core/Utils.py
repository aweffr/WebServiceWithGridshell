# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import shelve
from pprint import pprint
from math import floor
from scipy import interpolate
from scipy.optimize import brenth
from operator import itemgetter, attrgetter

def xlist(inlst):
    # inlst format:[(a1,b1), (a2,b2),....(an,bn)]
    # out format: [a1, a2, a3, ..., an]
    return map(lambda x: x[0], inlst)


def ylist(inlst):
    # inlst format same as xlist
    # out format: [b1, b2, b3, ..., bn]
    return map(lambda x: x[1], inlst)


def zlist(inlst):
    return map(lambda x: x[2], inlst)


def get_spl(inlst):
    # inlst format:[(a1,b1), (a2,b2),....(an,bn)]
    # before generate the spline, sort it by x_coord.
    # out: a spline object
    inlst = sorted(inlst, key=itemgetter(0))
    spl = interpolate.InterpolatedUnivariateSpline(xlist(inlst), ylist(inlst))
    return spl


def root(spl, y, start, stop, scan_step=0.05, DEBUG=1):
    out = []
    fun = lambda x: spl(x) - y
    for i in np.arange(start - 0.1, stop + 0.1, step=scan_step):
        if (fun(i) <= 0 < fun(i + scan_step)) or (fun(i) >= 0 > fun(i + scan_step)):
            x_val = float(brenth(fun, i, i + scan_step))
            out.append((x_val, y))
    if DEBUG:
        s = ['Finding root at y=%.1f' % y,
             "start=%.2f, stop=%.2f, scan_step=%.3f" % (start, stop, scan_step),
             'and root is %s' % str(out)]
        print " ".join(s)
    if len(out) % 2 != 0 and len(out) > 1:
        temp = []
        temp.append(out[0])
        x_last, y_last = out[0]
        for x, y in out[1:]:
            if abs(x - x_last) > 1.0:
                out.append((x, y))
                x_last, y_last = x, y
        out = temp
    if len(out) == 1:
        out = []
    return out


def generate_xcoord(spl, start, stop, step=1.0):
    out = []
    for x in np.arange(start + step, stop, step):
        y = float(spl(x))
        temp = [(x, y), (x, -y)]
        out.append(temp)
    return out


def generate_ycoord(spl, start, stop, step=1.0, *custom):
    if len(custom) == 2:
        x_c, y_c = custom
        out = [[(x_c, 0.0), (y_c, 0.0)], ]
    else:
        out = [[(start, 0.0), (stop, 0.0)], ]
        x_c, y_c = start, stop
    for y in np.arange(start + step, stop, step):
        temp = root(spl, y, x_c, y_c, scan_step=0.025)
        if len(temp) % 2 != 0:
            print temp
            raise Exception("Wrong Root List")
        if len(temp) == 0:
            break
        for i in range(0, len(temp), 2):
            temp1 = temp[i:i + 2]
            x1, x2 = temp1[0][0], temp1[1][0]
            mid = (x1 + x2 + 0.0) / 2
            diff = abs(spl(x1) + spl(x2) - 2 * spl(mid)) / 2
            print 'diff is', diff
            if diff < 0.2:
                continue
            out.append(temp[i:i + 2])
            temp2 = []
            for x, y in temp[i:i + 2]:
                temp2.append((x, -y))
            out.append(temp2)
    return out


def generate_incoord(spl, start=0.0, stop=60.0, step=1.0):
    out = []
    for x in np.arange(start + step, stop, step):
        y = floor(float(spl(x)) - 0.20)
        for yy in np.arange(-y, y + step, step):
            out.append((x, yy), )
    return out


def to_3d_xy(pointlst):
    # Input format:[ [(a1, b1), (a2, b2)],
    #                [(a3, b3), (a4, b4)],
    #                ......
    #                [......,   (an, bn)] ]
    # Output format:[(a1, b1, 0.0), (a2, b2, 0.0), ..., (an, bn, 0.0)]
    out = []
    for lst in pointlst:
        for x, y in lst:
            out.append((x, y, 0.0), )
    return out


def to_3d_in(pointlst):
    # Input format:[ (a1, b1), (a2, b2), ..., (an, bn)]
    # Output format:[ (a1, b1, 0.0), (a2, b2, 0.0), ..., (an, bn, 0.0)]
    out = []
    for x, y in pointlst:
        out.append((x, y, 0.0))
    return out


if __name__ == '__main__':
    # test unit
    test = [(0, 0), (7, 9.8), (16, 9), (27, 13), (36, 0)]
    spl = get_spl(test)
    xcoord = generate_xcoord(spl, 0, 36, 1.0)
    ycoord = generate_ycoord(spl, 0, 36, 1.0)
    incoord = generate_incoord(spl, 0, 36, 1.0)
    xcoord_3d = to_3d_xy(xcoord)
    ycoord_3d = to_3d_xy(ycoord)
    incoord_3d = to_3d_in(incoord)

    fig = plt.figure(figsize=(15, 8))
    plt.plot(xlist(test), ylist(test), 'r^', markersize=16)
    xx = np.linspace(0, 36, 1000)
    yy = spl(xx)
    plt.plot(xx, yy, 'r--', linewidth=6)
    for lst in xcoord + ycoord:
        plt.plot(xlist(lst), ylist(lst), linewidth=1.2)
    for x, y in incoord:
        plt.plot(x, y, 'ro', markersize=3.5)
    plt.xlim((-3.0, 39.0), )
    fig.savefig("initial_plain.png")
    plt.show()
