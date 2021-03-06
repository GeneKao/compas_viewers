from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.utilities import pairwise
from .node import Node


__all__ = ['CsgView', 'CsgObject']


class CsgObject(Node):

    def __init__(self, scene, datastructure, name=None, visible=True, settings={}, **kwargs):

        super(MeshObject, self).__init__()
        self.scene = scene
        self.datastructure = datastructure
        self.guid = None
        self.visible = visible
        self.view = CsgView(datastructure)
        self._settings = {}
        self._settings.update(settings)


    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        return self._settings.update(settings)



class CsgView(object):

    def __init__(self, mesh):
        self._mesh = None
        self._xyz = None
        self._vertices = None
        self._faces = None
        self.mesh = mesh

    @property
    def xyz(self):
        return self._xyz

    @property
    def vertices(self):
        key_index = self.mesh.key_index()
        return [key_index[key] for key in self.mesh.vertices()]

    @property
    def faces(self):
        return self._faces

    @property
    def edges(self):
        key_index = self.mesh.key_index()
        for u, v in self.mesh.edges():
            yield key_index[u], key_index[v]

    @property
    def mesh(self):
        return self._mesh

    @mesh.setter
    def mesh(self, mesh):
        self._mesh = mesh

        key_index = mesh.key_index()
        xyz = mesh.vertices_attributes('xyz')
        faces = []

        for fkey in mesh.faces():
            fvertices = [key_index[key] for key in mesh.face_vertices(fkey)]

            f = len(fvertices)
            if f < 3:
                pass
            elif f == 3:
                faces.append(fvertices)
            elif f == 4:
                a, b, c, d = fvertices
                faces.append([a, b, c])
                faces.append([c, d, a])
            else:
                o = mesh.face_centroid(fkey)
                v = len(xyz)
                xyz.append(o)
                for a, b in pairwise(fvertices + fvertices[0:1]):
                    faces.append([a, b, v])

        self._xyz = xyz
        self._faces = faces


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
