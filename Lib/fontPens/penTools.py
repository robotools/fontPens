import math

from fontTools.misc.py23 import *


def distance(pt1, pt2):
    """
    The distance between two points

    >>> distance((0, 0), (10, 0))
    10.0
    >>> distance((0, 0), (-10, 0))
    10.0
    >>> distance((0, 0), (0, 10))
    10.0
    >>> distance((0, 0), (0, -10))
    10.0
    >>> distance((10, 10), (13, 14))
    5.0
    """
    return math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)


def middlePoint(pt1, pt2):
    """
    Return the point that lies in between the two input points.
    """
    (x0, y0), (x1, y1) = pt1, pt2
    return 0.5 * (x0 + x1), 0.5 * (y0 + y1)


def getCubicPoint(t, pt0, pt1, pt2, pt3):
    if t == 0:
        return pt0
    if t == 1:
        return pt3
    if t == 0.5:
        a = middlePoint(pt0, pt1)
        b = middlePoint(pt1, pt2)
        c = middlePoint(pt2, pt3)
        d = middlePoint(a, b)
        e = middlePoint(b, c)
        return middlePoint(d, e)
    else:
        cx = (pt1[0] - pt0[0]) * 3
        cy = (pt1[1] - pt0[1]) * 3
        bx = (pt2[0] - pt1[0]) * 3 - cx
        by = (pt2[1] - pt1[1]) * 3 - cy
        ax = pt3[0] - pt0[0] - cx - bx
        ay = pt3[1] - pt0[1] - cy - by
        t3 = t ** 3
        t2 = t * t
        x = ax * t3 + bx * t2 + cx * t + pt0[0]
        y = ay * t3 + by * t2 + cy * t + pt0[1]
        return x, y


def getQuadraticPoint(t, pt0, pt1, pt2):
    if t == 0:
        return pt0
    if t == 1:
        return pt2
    a = (1 - t) ** 2
    b = 2 * (1 - t) * t
    c = t ** 2

    x = a * pt0[0] + b * pt1[0] + c * pt2[0];
    y = a * pt0[1] + b * pt1[1] + c * pt2[1];
    return x, y


def estimateCubicCurveLength(pt0, pt1, pt2, pt3, precision=10):
    """
    Estimate the length of this curve by iterating
    through it and averaging the length of the flat bits.
    """
    points = []
    length = 0
    step = 1.0 / precision
    factors = range(0, precision + 1)
    for i in factors:
        points.append(getCubicPoint(i * step, pt0, pt1, pt2, pt3))
    for i in range(len(points) - 1):
        pta = points[i]
        ptb = points[i + 1]
        length += distance(pta, ptb)
    return length


def estimateQuadraticCurveLength(pt0, pt1, pt2, precision=10):
    """
    Estimate the length of this curve by iterating
    through it and averaging the length of the flat bits.
    """
    points = []
    length = 0
    step = 1.0 / precision
    factors = range(0, precision + 1)
    for i in factors:
        points.append(getQuadraticPoint(i * step, pt0, pt1, pt2))
    for i in range(len(points) - 1):
        pta = points[i]
        ptb = points[i + 1]
        length += distance(pta, ptb)
    return length


def interpolatePoint(pt1, pt2, v):
    """
    interpolate point by factor v

    >>> interpolatePoint((0, 0), (10, 10), 0.5)
    (5.0, 5.0)
    >>> interpolatePoint((0, 0), (10, 10), 0.6)
    (6.0, 6.0)
    """
    (xa, ya), (xb, yb) = pt1, pt2
    if not isinstance(v, tuple):
        xv = v
        yv = v
    else:
        xv, yv = v
    return xa + (xb - xa) * xv, ya + (yb - ya) * yv


if __name__ == "__main__":
    import doctest
    doctest.testmod()
