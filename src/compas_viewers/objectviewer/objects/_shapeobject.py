from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.utilities import pairwise
from .node import Node


__all__ = ['ShapeView', 'ShapeObject']


class ShapeObject(Node):

    def __init__(self, scene, shape, name=None, visible=True, settings={}, **kwargs):
        
        super(ShapeObject, self).__init__()

        self.scene = scene
        self.shape = shape
        self.name = name
        self.guid = None
        self.visible = visible

        self.view = ShapeView(shape)
        self._settings = {}
        self._settings.update(settings)
        self.name = self.name or self.shape.__class__.__name__

    def to_data(self):
        return self.shape.to_data()

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        return self._settings.update(settings)



class ShapeView(object):

    def __init__(self, shape):
        self._shape = None
        self.shape = shape

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
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
