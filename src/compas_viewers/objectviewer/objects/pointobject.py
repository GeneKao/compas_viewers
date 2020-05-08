from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from ._primitiveobject import PrimitiveObject
from ._primitiveobject import PrimitiveView


__all__ = ['PointView', 'PointObject']


class PointObject(PrimitiveObject):

    def __init__(self, scene, primitive, name=None, visible=True, settings={}, **kwargs):
        super(PointObject,self).__init__(scene, primitive, **kwargs)
        self.view = PointView(primitive)

class PointView(PrimitiveView):

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
        return [0]

    @property
    def faces(self):
        return []

    @property
    def edges(self):
        return []

    @property
    def primitive(self):
        return self._primitive

    @primitive.setter
    def primitive(self, point):
        self._primitive = point
        xyz = [list(point)]
        self._xyz = xyz


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
