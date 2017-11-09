from __future__ import division
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
    """
    Return the point for t on the cubic curve defined by pt0, pt1, pt2, pt3.

    >>> getCubicPoint(0.00, (0, 0), (50, -10), (80, 50), (120, 40))
    (0, 0)
    >>> getCubicPoint(0.20, (0, 0), (50, -10), (80, 50), (120, 40))
    (27.84, 1.280000000000002)
    >>> getCubicPoint(0.50, (0, 0), (50, -10), (80, 50), (120, 40))
    (63.75, 20.0)
    >>> getCubicPoint(0.85, (0, 0), (50, -10), (80, 50), (120, 40))
    (102.57375, 40.2475)
    >>> getCubicPoint(1.00, (0, 0), (50, -10), (80, 50), (120, 40))
    (120, 40)
    """
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
    """
    Return the point for t on the quadratic curve defined by pt0, pt1, pt2, pt3.

    >>> getQuadraticPoint(0.00, (0, 0), (50, -10), (80, 50))
    (0, 0)
    >>> getQuadraticPoint(0.21, (0, 0), (50, -10), (80, 50))
    (20.118, -1.113)
    >>> getQuadraticPoint(0.50, (0, 0), (50, -10), (80, 50))
    (45.0, 7.5)
    >>> getQuadraticPoint(0.87, (0, 0), (50, -10), (80, 50))
    (71.862, 35.583)
    >>> getQuadraticPoint(1.00, (0, 0), (50, -10), (80, 50))
    (80, 50)
    """
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

    >>> estimateCubicCurveLength((0, 0), (0, 0), (0, 0), (0, 0), 10)
    0.0
    >>> estimateCubicCurveLength((0, 0), (0, 0), (120, 0), (120, 0), 10)
    120.0
    >>> estimateCubicCurveLength((0, 0), (50, 0), (80, 0), (120, 0), 10)
    120.0
    >>> estimateCubicCurveLength((0, 0), (50, -10), (80, 50), (120, 40), 1)
    126.49110640673517
    >>> estimateCubicCurveLength((0, 0), (50, -10), (80, 50), (120, 40), 10)
    130.26123149406607
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

    >>> estimateQuadraticCurveLength((0, 0), (0, 0), (0, 0)) # empty segment
    0.0
    >>> estimateQuadraticCurveLength((0, 0), (50, 0), (80, 0)) # collinear points
    80.0
    >>> estimateQuadraticCurveLength((0, 0), (50, 20), (100, 40)) # collinear points
    107.70329614269008
    >>> estimateQuadraticCurveLength((0, 0), (40, 0), (-40, 0)) # collinear points, control point outside
    66.39999999999999
    >>> estimateQuadraticCurveLength((0, 0), (40, 0), (0, 0)) # collinear points, looping back
    40.0
    >>> estimateQuadraticCurveLength((0, 0), (0, 100), (100, 0))
    153.6861437729263
    >>> estimateQuadraticCurveLength((0, 0), (50, -10), (80, 50))
    102.4601733446439
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


def getQuadraticCurveLength(pt0, pt1, pt2, precision=10):
    """
    Calculate the length of a quadratic curve.
    Source: http://www.malczak.linuxpl.com/blog/quadratic-bezier-curve-length/

    >>> getQuadraticCurveLength((0, 0), (0, 0), (0, 0)) # empty segment
    0.0
    >>> getQuadraticCurveLength((0, 0), (50, 0), (80, 0)) # collinear points
    80.0
    >>> getQuadraticCurveLength((0, 0), (0, 50), (0, 80)) # collinear points vertical
    80.0
    >>> getQuadraticCurveLength((0, 0), (50, 20), (100, 40)) # collinear points
    107.70329614269008
    >>> getQuadraticCurveLength((0, 0), (40, 0), (-40, 0)) # collinear points, control point outside
    66.6666666666667
    >>> getQuadraticCurveLength((0, 0), (40, 0), (0, 0)) # collinear points, looping back
    40.0
    >>> getQuadraticCurveLength((0, 0), (0, 100), (100, 0))
    154.02976155645263
    >>> getQuadraticCurveLength((0, 0), (0, 50), (100, 0))
    120.21581243984076
    >>> getQuadraticCurveLength((0, 0), (50, -10), (80, 50))
    102.53273816445825
    """
    if pt0 == pt1 or pt1 == pt2:
        if pt0 == pt2:
            return 0.0
        return distance(pt0, pt2)
    
    ax = pt0[0] - 2 * pt1[0] + pt2[0]
    ay = pt0[1] - 2 * pt1[1] + pt2[1]
    bx = 2 * pt1[0] - 2 * pt0[0]
    by = 2 * pt1[1] - 2 * pt0[1]
    
    A = 4 * (ax * ax + ay * ay)
    B = 4 * (ax * bx + ay * by)
    C = bx * bx + by * by
    
    if A == 0:
        if B == 0:
            if C == 0:
                # Empty curve
                length = 0.0
            else:
                # Line
                length = distance(pt0, pt2)
        else:
            # Can this happen? The tests don't trigger it
            return estimateQuadraticCurveLength(pt0, pt1, pt2, precision)
            Sabc = 2 * math.sqrt(B + C)
            C_2 = 2 * math.sqrt(C)
            BA = B / 0

            length = (
                (- B * B) * math.log((BA + Sabc) / (BA + C_2)) 
            ) / 0
    else:
        if B == 0:
            Sabc = 2 * math.sqrt(A + C)
            A_32 = 2 * A * math.sqrt(A)

            length = A_32 * Sabc / (4 * A_32)
        else:
            Sabc = 2 * math.sqrt(A + B + C)
            A_2 = math.sqrt(A)
            A_32 = 2 * A * A_2
            C_2 = 2 * math.sqrt(C)
            BA = B / A_2

            if BA + C_2 == 0:
                # The points are collinear, but may be in usual order
                # Fall back to estimated curve length
                return estimateQuadraticCurveLength(pt0, pt1, pt2, precision)
            else:
                length = (
                    A_32 * Sabc + 
                    A_2 * B * (Sabc - C_2) + 
                    (4 * C * A - B * B) * math.log((2 * A_2 + BA + Sabc) / (BA + C_2)) 
                ) / (4 * A_32)
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
