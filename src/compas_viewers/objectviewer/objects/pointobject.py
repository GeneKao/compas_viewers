from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from ._primitiveobject import PrimitiveObject
from ._primitiveobject import PrimitiveView


__all__ = ['PointView', 'PointObject']


class PointObject(PrimitiveObject):

    def __init__(self, scene, point, **kwargs):
        super(PointObject,self).__init__(scene, point, **kwargs)
        self.view = PointView(point)

class PointView(PrimitiveView):

    @property
    def vertices(self):
        return [0]

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
