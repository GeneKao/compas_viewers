from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.utilities import pairwise
from ._primitiveobject import PrimitiveObject
from ._primitiveobject import PrimitiveView
from .pointobject import PointObject


__all__ = ['LineView', 'LineObject']


class LineObject(PrimitiveObject):

    def __init__(self, scene, line, **kwargs):

        super(LineObject,self).__init__(scene, line, **kwargs)
        
        self.start = PointObject(scene, line.start)
        self.end = PointObject(scene, line.end)
        # self.add(self.start)
        # self.add(self.end)

        self.view = LineView(line)

class LineView(PrimitiveView):
    @property
    def vertices(self):
        return [0, 1]

    @property
    def edges(self):
        return [[0, 1]]

    @property
    def primitive(self):
        return self._primitive

    @primitive.setter
    def primitive(self, line):
        self._primitive = line
        xyz = [list(line.start), list(line.end)]
        self._xyz = xyz


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
