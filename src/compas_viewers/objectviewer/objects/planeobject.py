from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.utilities import pairwise
from ._primitiveobject import PrimitiveObject
from ._primitiveobject import PrimitiveView
from .pointobject import PointObject

import numpy as np


__all__ = ['PlaneView', 'PlaneObject']


class PlaneObject(PrimitiveObject):

    def __init__(self, scene, plane, **kwargs):
        super(PlaneObject,self).__init__(scene, plane, **kwargs)

        self.origin = PointObject(scene, plane.point)
        self.add(self.origin)

        self.view = PlaneView(plane)

class PlaneView(PrimitiveView):

    def __init__(self, plane, size=1):

        self.size = size
        self.points = []
        super(PlaneView,self).__init__(plane)

    def _evaluate_plane(self, x, y, z):
        x_axis = np.array([1,0,0])
        z_axis = np.array(self.primitive.normal)
        z_axis /= np.linalg.norm(z_axis)
        if np.linalg.norm(x_axis - z_axis) <= 0.1 or np.linalg.norm(x_axis - z_axis) >= 1.9:
            x_axis = np.array([0,1,0])
        y_axis = np.cross(z_axis,x_axis)
        x_axis = np.cross(y_axis,z_axis)
        plane_pt = np.array(self.primitive.point)
        return (x*x_axis + y*y_axis + z*z_axis)*self.size + plane_pt

    @property
    def edges(self):
        return [[i, i+1] for i,_ in list(enumerate(self.points))[:-1]]

    @property
    def primitive(self):
        return self._primitive

    @primitive.setter
    def primitive(self, polyline):
        self._primitive = polyline
        self.points = [[-1,-1,0], [1,-1,0], [1,1,0], [-1,1,0], [-1,-1,0]]
        xyz = [ self._evaluate_plane(*pt) for pt in self.points]
        self._xyz = xyz


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass