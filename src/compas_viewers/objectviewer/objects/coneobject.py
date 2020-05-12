from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from ._shapeobject import ShapeObject
from ._shapeobject import ShapeView
from .pointobject import PointObject


import numpy as np
import math

__all__ = ['ConeView', 'ConeObject']


class ConeObject(ShapeObject):

    def __init__(self, scene, cone, segments=5, **kwargs):
        super(ConeObject,self).__init__(scene, cone, **kwargs)
        
        self.center = PointObject(scene, cone.plane.point)
        self.add(self.center)

        self.view = ConeView(cone, segments)

class ConeView(ShapeView):

    def __init__(self, cone, segments=5):

        self.points = []
        self.segments = segments
        super(ConeView,self).__init__(cone)
        

    def _evaluate_circle(self, x, y, z):
        x_axis = np.array([1,0,0])
        z_axis = np.array(self.shape.plane.normal)
        z_axis /= np.linalg.norm(z_axis)
        if np.linalg.norm(x_axis - z_axis) <= 0.1 or np.linalg.norm(x_axis - z_axis) >= 1.9:
            x_axis = np.array([0,1,0])
        y_axis = np.cross(z_axis,x_axis)
        x_axis = np.cross(y_axis,z_axis)
        plane_pt = np.array(self.shape.plane.point)
        return (x*x_axis + y*y_axis)*self.shape.radius + z*z_axis + plane_pt


    @property
    def faces(self):
        return [[0, i, i+1] for i,_ in list(enumerate(self.points))[2:-1]] + [[1, i, i+1] for i,_ in list(enumerate(self.points))[2:-1]]

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, cone):
        self._shape = cone
        
        self.points = [[0,0,0],[0,0,cone.height]]
        self.points += [[math.cos((i/self.segments)*math.pi*2),math.sin((i/self.segments)*math.pi*2),0] for i in range(self.segments)]
        self.points.append(self.points[2])
        
        xyz = [ self._evaluate_circle(*pt) for pt in self.points]
        self._xyz = xyz


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass