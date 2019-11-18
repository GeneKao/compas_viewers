from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_viewers.core import App

from compas_viewers.multimeshviewer.view import View
from compas_viewers.multimeshviewer.controller import Controller

from compas_viewers.multimeshviewer import CONFIG
from compas_viewers.multimeshviewer import STYLE


__all__ = ['MultiMeshViewer']


class MultiMeshViewer(App):
    """"""

    def __init__(self):
        super().__init__(CONFIG, STYLE)
        self._meshes = None
        self.controller = Controller(self)
        self.view = View(self.controller)
        self.view.camera.events.rotX.connect(self.controller.on_rotX)
        self.view.camera.events.rotZ.connect(self.controller.on_rotZ)
        self.view.camera.events.distance.connect(self.controller.on_distance)
        self.setup()
        self.init()
        self.view.glInit()
        self.view.setup_grid()
        self.view.setup_axes()

    @property
    def meshes(self):
        return self.controller.meshes

    @meshes.setter
    def meshes(self, meshes):
        self.controller.meshes = meshes
        self.controller.center()
        self.view.glInit()
        self.view.make_buffers()
        self.view.updateGL()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    # each object has a mesh and a transformation stack
    # the transformation stack applies to the local coordinate system of the object
    # this transformation stack becomes the "model" matrix
    # the "model" transformation is applied first
    # to each mesh individually
    # the "view" matrix is uniform (same everywhere)
    # the "projection" transformation is uniform

    from compas.geometry import Box
    from compas.datastructures import Mesh
    from compas.datastructures import mesh_subdivide_quad
    from compas.datastructures import mesh_quads_to_triangles

    box = Box.from_width_height_depth(5.0, 3.0, 1.0)
    a = Mesh.from_vertices_and_faces(box.vertices, box.faces)
    a = mesh_subdivide_quad(a, k=2)
    mesh_quads_to_triangles(a)

    box = Box.from_width_height_depth(1.0, 5.0, 3.0)
    b = Mesh.from_vertices_and_faces(box.vertices, box.faces)
    b = mesh_subdivide_quad(b, k=2)

    viewer = MultiMeshViewer()
    viewer.meshes = [a, b]

    viewer.show()
