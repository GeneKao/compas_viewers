from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_viewers.core import App

from compas_viewers.meshviewer.view import View
from compas_viewers.meshviewer.controller import Controller

from compas_viewers.meshviewer import CONFIG
from compas_viewers.meshviewer import STYLE


__all__ = ['MeshViewer']


class MeshViewer(App):
    """"""

    def __init__(self):
        super(MeshViewer, self).__init__(CONFIG, STYLE)
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
    def mesh(self):
        return self.controller.mesh

    @mesh.setter
    def mesh(self, mesh):
        self.controller.mesh = mesh
        self.controller.center_mesh()
        self.view.glInit()
        self.view.make_buffers()
        self.view.updateGL()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.datastructures import Mesh

    viewer = MeshViewer()
    viewer.mesh = Mesh.from_polyhedron(6)

    viewer.show()
