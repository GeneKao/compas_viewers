from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from ._shapeobject import ShapeObject
from ._shapeobject import ShapeView

from compas.geometry import Point
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Circle
from .pointobject import PointObject
from .lineobject import LineObject


from compas.geometry import Cone
from .coneobject import ConeObject

import numpy as np
import math

__all__ = ['ArrowView', 'ArrowObject']


class ArrowObject(ShapeObject):

    def __init__(self, scene, arrow, **kwargs):
        super(ArrowObject,self).__init__(scene, arrow, **kwargs)

        length = np.linalg.norm(arrow.direction)

        plane = Plane(arrow.point + arrow.direction*0.7, arrow.direction)
        circle = Circle(plane, length*0.15)
        cone = Cone(circle, length*0.3)

        line = Line(Point(*arrow.point), Point(*(arrow.point + arrow.direction*0.7)))
        
        self.view = ArrowView(arrow, ConeObject(None, cone, 3), LineObject(None, line))

class ArrowView(ShapeView):

    def __init__(self, arrow, coneobject, lineobject):

        self.coneobject = coneobject
        self.lineobject = lineobject
        super(ArrowView,self).__init__(arrow)

    @property
    def edges(self):
        return self.lineobject.view.edges

    @property
    def faces(self):
        faces = np.array(self.coneobject.view.faces) + len(self.lineobject.view.xyz)
        return faces

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, arrow):
        print(arrow.point)
        self._shape = arrow
        self._xyz = self.lineobject.view.xyz + self.coneobject.view.xyz


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass