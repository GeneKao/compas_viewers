from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.utilities import pairwise
from .node import Node

__all__ = ['NetworkView', 'NetworkObject']


class NetworkObject(Node):

    def __init__(self, scene, datastructure, name=None, visible=True, settings={}, **kwargs):

        super(NetworkObject, self).__init__()
        self.scene = scene
        self.datastructure = datastructure
        self.name = name
        self.guid = None
        self.visible = visible
        # self.artist = None
        self.view = NetworkView(datastructure)
        self._settings = {}
        self._settings.update(settings)


    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        return self._settings.update(settings)



class NetworkView(object):

    def __init__(self, network):
        self._network = None
        self._xyz = None
        self._vertices = None
        self._faces = None
        self.network = network

    @property
    def xyz(self):
        return self._xyz

    @property
    def vertices(self):
        key_index = self.network.key_index()
        return [key_index[key] for key in self.network.nodes()]

    @property
    def vertices_color(self):
        return [color or (0, 0, 0) for color in self.network.nodes_attribute('color')]

    @property
    def faces(self):
        return self._faces

    @property
    def edges(self):
        key_index = self.network.key_index()
        for u, v in self.network.edges():
            yield key_index[u], key_index[v]

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, network):
        self._network = network

        key_index = network.key_index()
        xyz = network.nodes_attributes('xyz')

        self._xyz = xyz
        self._faces = []


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
