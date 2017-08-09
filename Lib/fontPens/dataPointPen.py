from fontTools.misc.py23 import *
from ufoLib.pointPen import AbstractPointPen, PointToSegmentPen


class DataPointPen(AbstractPointPen):
    """
    A point pen that collects all data and can draw it back into an other pen.
    """

    def __init__(self):
        self.contourData = list()
        self.componentsData = list()

    def beginPath(self, identifier=None):
        self.contourData.append((list(), identifier))

    def addPoint(self, *args, **kwargs):
        self.contourData[-1][0].append((args, kwargs))

    def endPath(self):
        pass

    def addComponent(self, *args, **kwargs):
        self.componentsData.append((args, kwargs))

    def drawPoints(self, pointPen):
        pointPen.skipConflictingIdentifiers = True
        for contourData, identifier in self.contourData:
            pointPen.beginPath(identifier=identifier)
            for contourArgs, contourKwargs in contourData:
                pointPen.addPoint(*contourArgs, **contourKwargs)
            pointPen.endPath()
        for componentArgs, componentKwargs in self.componentsData:
            pointPen.addComponent(*componentArgs, **componentKwargs)

    def draw(self, pen):
        self.drawPoints(PointToSegmentPen(pen))


def _testPointDataPen():
    """
    >>> from printPointPen import PrintPointPen
    >>> from printPen import PrintPen

    >>> pen = DataPointPen()
    >>> pen.beginPath()
    >>> pen.addPoint((0, 0), True, name="hello")
    >>> pen.endPath()
    >>> pen.drawPoints(PrintPointPen())
    pen.beginPath()
    pen.addPoint((0, 0), segmentType=True, name='hello')
    pen.endPath()

    >>> pen.beginPath()
    >>> pen.addPoint((1, 1), False, name="world")
    >>> pen.endPath()
    >>> pen.drawPoints(PrintPointPen())
    pen.beginPath()
    pen.addPoint((0, 0), segmentType=True, name='hello')
    pen.endPath()
    pen.beginPath()
    pen.addPoint((1, 1), segmentType=False, name='world')
    pen.endPath()

    >>> pen.draw(PrintPen())
    pen.moveTo((0, 0))
    pen.endPath()
    pen.moveTo((1, 1))
    pen.endPath()
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
