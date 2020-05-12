from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from ._shapeobject import ShapeObject
from ._shapeobject import ShapeView


__all__ = ['PolyhedronView', 'PolyhedronObject']


class PolyhedronObject(ShapeObject):

    def __init__(self, scene, polyhedron, **kwargs):
        super(PolyhedronObject,self).__init__(scene, polyhedron, **kwargs)
        self.view = PolyhedronView(polyhedron)

class PolyhedronView(ShapeView):

    @property
    def faces(self):
        return self._shape.faces

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, polyhedron):
        self._shape = polyhedron
        self._xyz = polyhedron.vertices


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass