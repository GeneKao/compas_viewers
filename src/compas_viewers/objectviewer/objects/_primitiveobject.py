from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.utilities import pairwise
from .node import Node


__all__ = ['PrimitiveView', 'PrimitiveObject']


class PrimitiveObject(Node):

    def __init__(self, scene, primitive, **kwargs):
        super(PrimitiveObject, self).__init__(**kwargs)
        self.scene = scene
        self.primitive = primitive
        self.view = PrimitiveView(primitive)



class PrimitiveView(object):

    def __init__(self, primitive):
        self._primitive = None
        self.primitive = primitive

    @property
    def xyz(self):
        return self._xyz

    @property
    def vertices(self):
        return []

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
    def primitive(self, primitive):
        self._primitive = primitive


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
