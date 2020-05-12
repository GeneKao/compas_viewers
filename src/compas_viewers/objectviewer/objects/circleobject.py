from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.utilities import pairwise
from ._primitiveobject import PrimitiveObject
from ._primitiveobject import PrimitiveView
from .pointobject import PointObject

import numpy as np
import math

__all__ = ['CircleView', 'CircleObject']


class CircleObject(PrimitiveObject):

    def __init__(self, scene, circle, **kwargs):
        super(CircleObject,self).__init__(scene, circle, **kwargs)
        
        self.center = PointObject(scene, circle.plane.point)
        self.add(self.center)

        self.view = CircleView(circle)

class CircleView(PrimitiveView):

    def __init__(self, circle, segments=20):

        self.points = []
        self.segments = segments
        super(CircleView,self).__init__(circle)
        

    def _evaluate_circle(self, x, y, z):
        x_axis = np.array([1,0,0])
        z_axis = np.array(self.primitive.plane.normal)
        z_axis /= np.linalg.norm(z_axis)
        if np.linalg.norm(x_axis - z_axis) <= 0.1 or np.linalg.norm(x_axis - z_axis) >= 1.9:
            x_axis = np.array([0,1,0])
        y_axis = np.cross(z_axis,x_axis)
        x_axis = np.cross(y_axis,z_axis)
        plane_pt = np.array(self.primitive.plane.point)
        return (x*x_axis + y*y_axis + z*z_axis)*self.primitive.radius + plane_pt

    @property
    def edges(self):
        return [[i, i+1] for i,_ in list(enumerate(self.points))[:-1]]

    @property
    def primitive(self):
        return self._primitive

    @primitive.setter
    def primitive(self, polyline):
        self._primitive = polyline
        
        self.points = [[math.cos((i/self.segments)*math.pi*2),math.sin((i/self.segments)*math.pi*2),0] for i in range(self.segments)]
        self.points.append(self.points[0])
        
        xyz = [ self._evaluate_circle(*pt) for pt in self.points]
        self._xyz = xyz


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass