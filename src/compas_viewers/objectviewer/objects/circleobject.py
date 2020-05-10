from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.utilities import pairwise
from ._primitiveobject import PrimitiveObject
from ._primitiveobject import PrimitiveView

import numpy as np
import math

__all__ = ['CircleView', 'CircleObject']


class CircleObject(PrimitiveObject):

    def __init__(self, scene, primitive, name=None, visible=True, settings={}, **kwargs):
        super(CircleObject,self).__init__(scene, primitive, **kwargs)
        self.view = CircleView(primitive)

class CircleView(PrimitiveView):

    def __init__(self, primitive):
        self._primitive = None
        self._xyz = None
        self._vertices = None
        self._faces = None
        self.points = []
        self.segments = 20
        self.primitive = primitive

    def _evaluate_circle(self, x, y, z):
        x_axis = np.array([1,0,0])
        z_axis = np.array(self.primitive.plane.normal)
        z_axis /= np.linalg.norm(z_axis)
        if np.linalg.norm(x_axis - z_axis) == 0:
            x_axis = np.array([0,1,0])
        y_axis = np.cross(z_axis,x_axis)
        x_axis = np.cross(y_axis,z_axis)

        plane_pt = np.array(self.primitive.plane.point)

        return (x*x_axis + y*y_axis + z*z_axis)*self.primitive.radius + plane_pt

    @property
    def xyz(self):
        return self._xyz

    @property
    def vertices(self):
        return [0]

    @property
    def faces(self):
        return []

    @property
    def edges(self):
        edge_pts = []
        return [[i, i+1] for i,_ in list(enumerate(self.points))[1:-1]]

    @property
    def primitive(self):
        return self._primitive

    @primitive.setter
    def primitive(self, polyline):
        self._primitive = polyline
        
        self.points = [[0,0,0]]
        self.points += [[math.cos((i/self.segments)*math.pi*2),math.sin((i/self.segments)*math.pi*2),0] for i in range(self.segments)]
        self.points.append(self.points[1])
        
        xyz = [ self._evaluate_circle(*pt) for pt in self.points]
        self._xyz = xyz


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass