from __future__ import print_function, division

from fontTools.misc.py23 import *
from ufoLib.pointPen import AbstractPointPen


class PrintPointPen(AbstractPointPen):
    """
    A PointPen that prints every step.
    """

    def __init__(self):
        self.havePath = False

    def beginPath(self, identifier=None):
        self.havePath = True
        if identifier is not None:
            print("pen.beginPath(identifier=%r)" % identifier)
        else:
            print("pen.beginPath()")

    def endPath(self):
        self.havePath = False
        print("pen.endPath()")

    def addPoint(self, pt, segmentType=None, smooth=False, name=None, identifier=None, **kwargs):
        assert self.havePath
        args = ["(%s, %s)" % (pt[0], pt[1])]
        if segmentType is not None:
            args.append("segmentType=%r" % segmentType)
        if smooth:
            args.append("smooth=True")
        if name is not None:
            args.append("name=%r" % name)
        if identifier is not None:
            args.append("identifier=%r" % identifier)
        if kwargs:
            args.append("**%s" % kwargs)
        print("pen.addPoint(%s)" % ", ".join(args))

    def addComponent(self, baseGlyphName, transformation, identifier=None):
        assert not self.havePath
        print("pen.addComponent(%r, %s, %r)" % (baseGlyphName, tuple(transformation), identifier))


def _testPrintPointPen():
    """
    >>> pen = PrintPointPen()
    >>> pen.beginPath()
    pen.beginPath()
    >>> pen.beginPath("abc123")
    pen.beginPath(identifier='abc123')
    >>> pen.addPoint((10, 10), "curve", True, identifier="abc123")
    pen.addPoint((10, 10), segmentType='curve', smooth=True, identifier='abc123')
    >>> pen.endPath()
    pen.endPath()
    >>> pen.addComponent("a", (1, 0, 0, 1, 10, 10), "xyz987")
    pen.addComponent('a', (1, 0, 0, 1, 10, 10), 'xyz987')
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
