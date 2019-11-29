from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_viewers.core import App

from compas_viewers.multimeshviewer.model import MeshObject
from compas_viewers.multimeshviewer.view import View
from compas_viewers.multimeshviewer.controller import Controller

from compas_viewers.multimeshviewer.settings import SETTINGS
from compas_viewers.multimeshviewer.ui import UI
from compas_viewers.multimeshviewer.style import STYLE


__all__ = ['MultiMeshViewer']


class MultiMeshViewer(App):
    """"""

    def __init__(self):
        super().__init__(SETTINGS, UI, STYLE)
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
    def colors(self):
        return self.controller.colors

    @colors.setter
    def colors(self, colors):
        self.controller.colors = colors

    @property
    def meshes(self):
        return self.controller.meshes

    @meshes.setter
    def meshes(self, meshes):
        temp = []
        for mesh in meshes:
            if not isinstance(mesh, MeshObject):
                mesh = MeshObject(mesh)
            temp.append(mesh)
        self.controller.meshes = temp
        # self.controller.center()
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

    import random

    from math import radians

    from compas.geometry import Box
    from compas.datastructures import Mesh
    from compas.datastructures import mesh_transform_numpy
    from compas.utilities import rgb_to_hex
    from compas.geometry import Translation
    from compas.geometry import Rotation

    meshes = []

    for i in range(10):
        vector = [random.randint(0, 10), random.randint(0, 10), random.randint(0, 5)]
        T = Translation(vector)
        axis = [0, 0, 1.0]
        angle = radians(random.randint(0, 180))
        R = Rotation.from_axis_and_angle(axis, angle)
        X = T * R
        w, h, d = random.randint(1, 3), random.randint(1, 3), random.randint(1, 3)
        box = Box.from_width_height_depth(w, h, d)
        mesh = Mesh.from_shape(box)
        mesh_transform_numpy(mesh, X)
        rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        obj = MeshObject(mesh, color=rgb_to_hex(rgb))
        meshes.append(obj)

    viewer = MultiMeshViewer()
    viewer.meshes = meshes

    viewer.show()
