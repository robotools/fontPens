from __future__ import absolute_import, print_function, division

from fontTools.misc.py23 import *
from fontTools.pens.basePen import AbstractPen


class PrintPen(AbstractPen):
    """
    A SegmentPen that prints every step.
    """

    def moveTo(self, pt):
        print("pen.moveTo(%s)" % (pt,))

    def lineTo(self, pt):
        print("pen.lineTo(%s)" % (pt,))

    def curveTo(self, *pts):
        print("pen.curveTo%s" % (pts,))

    def qCurveTo(self, *pts):
        print("pen.qCurveTo%s" % (pts,))

    def closePath(self):
        print("pen.closePath()")

    def endPath(self):
        print("pen.endPath()")

    def addComponent(self, baseGlyphName, transformation):
        print("pen.addComponent('%s', %s)" % (baseGlyphName, tuple(transformation)))


def _testPrintPen():
    """
    >>> pen = PrintPen()
    >>> pen.moveTo((10, 10))
    pen.moveTo((10, 10))
    >>> pen.lineTo((20, 20))
    pen.lineTo((20, 20))
    >>> pen.curveTo((1, 1), (2, 2), (3, 3))
    pen.curveTo((1, 1), (2, 2), (3, 3))
    >>> pen.qCurveTo((4, 4), (5, 5))
    pen.qCurveTo((4, 4), (5, 5))
    >>> pen.closePath()
    pen.closePath()
    >>> pen.endPath()
    pen.endPath()
    >>> pen.addComponent("a", (1, 0, 0, 1, 10, 10))
    pen.addComponent('a', (1, 0, 0, 1, 10, 10))
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
