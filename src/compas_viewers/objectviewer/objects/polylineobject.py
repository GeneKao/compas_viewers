from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.utilities import pairwise
from ._primitiveobject import PrimitiveObject
from ._primitiveobject import PrimitiveView
from .pointobject import PointObject

__all__ = ['PolylineView', 'PolylineObject']


class PolylineObject(PrimitiveObject):

    def __init__(self, scene, polyline, **kwargs):
        super(PolylineObject,self).__init__(scene, polyline, **kwargs)
        self.points = [PointObject(scene, point) for point in polyline.points]
        for point in self.points:
            self.add(point)
        self.view = PolylineView(polyline)

class PolylineView(PrimitiveView):

    @property
    def edges(self):
        return [[i, i+1] for i,_ in list(enumerate(self.primitive.points))[:-1]]

    @property
    def primitive(self):
        return self._primitive

    @primitive.setter
    def primitive(self, polyline):
        self._primitive = polyline
        xyz = [list(point) for point in polyline.points]
        self._xyz = xyz


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
