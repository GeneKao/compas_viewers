from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.utilities import pairwise
from ._primitiveobject import PrimitiveObject
from ._primitiveobject import PrimitiveView


__all__ = ['PolylineView', 'PolylineObject']


class PolylineObject(PrimitiveObject):

    def __init__(self, scene, primitive, name=None, visible=True, settings={}, **kwargs):
        super(PolylineObject,self).__init__(scene, primitive, **kwargs)
        self.view = PolylineView(primitive)

class PolylineView(PrimitiveView):

    def __init__(self, primitive):
        self._primitive = None
        self._xyz = None
        self._vertices = None
        self._faces = None
        self.primitive = primitive

    @property
    def xyz(self):
        return self._xyz

    @property
    def vertices(self):
        return [i for i,_ in enumerate(self.primitive.points)]

    @property
    def faces(self):
        return []

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
