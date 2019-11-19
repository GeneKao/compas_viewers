from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial

from random import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from compas.utilities import hex_to_rgb
from compas.utilities import flatten
from compas_viewers.core import GLWidget
from compas_viewers.core import Grid
from compas_viewers.core import Axes


__all__ = ['View']


hex_to_rgb = partial(hex_to_rgb, normalize=True)


def flist(items):
    return list(flatten(items))


class View(GLWidget):
    """"""

    def __init__(self, controller):
        super(View, self).__init__()
        self.controller = controller
        self.n = 0
        self.v = 0
        self.e = 0
        self.f = 0

    @property
    def meshes(self):
        return self.controller.meshes

    @property
    def settings(self):
        return self.controller.settings

    # ==========================================================================
    # CAD
    # ==========================================================================

    def setup_grid(self):
        grid = Grid()
        index = glGenLists(1)
        glNewList(index, GL_COMPILE)
        grid.draw()
        glEndList()
        self.display_lists.append(index)

    def setup_axes(self):
        axes = Axes()
        index = glGenLists(1)
        glNewList(index, GL_COMPILE)
        axes.draw()
        glEndList()
        self.display_lists.append(index)

    # ==========================================================================
    # painting
    # ==========================================================================

    def paint(self):
        glDisable(GL_DEPTH_TEST)
        for dl in self.display_lists:
            glCallList(dl)

        glEnable(GL_DEPTH_TEST)
        self.draw_buffers()

    def make_buffers(self):
        self.buffers = []
        for m in self.meshes:
            xyz = flist(m.view.xyz)
            vertices = list(m.view.vertices)
            edges = flist(m.view.edges)
            faces = flist(m.view.faces)
            faces_back = flist(face[::-1] for face in m.view.faces)
            vertices_color = flist(hex_to_rgb('#000000') for key in m.view.vertices)
            edges_color = flist(hex_to_rgb('#333333') for key in m.view.edges)
            faces_color = flist(hex_to_rgb(m.color) for key in m.view.xyz)
            faces_color_back = flist(hex_to_rgb(m.color) for key in m.view.xyz)
            self.buffers.append({
                'xyz': self.make_vertex_buffer(xyz),
                'vertices': self.make_index_buffer(vertices),
                'edges': self.make_index_buffer(edges),
                'faces': self.make_index_buffer(faces),
                'faces:back': self.make_index_buffer(faces_back),
                'vertices.color': self.make_vertex_buffer(vertices_color, dynamic=True),
                'edges.color': self.make_vertex_buffer(edges_color, dynamic=True),
                'faces.color': self.make_vertex_buffer(faces_color, dynamic=True),
                'faces.color:back': self.make_vertex_buffer(faces_color_back, dynamic=True),
                'n': len(xyz),
                'v': len(vertices),
                'e': len(edges),
                'f': len(faces)})

    def draw_buffers(self):
        if not self.buffers:
            return

        for buffer in self.buffers:
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_COLOR_ARRAY)
            glBindBuffer(GL_ARRAY_BUFFER, buffer['xyz'])
            glVertexPointer(3, GL_FLOAT, 0, None)

            if self.settings['faces.on']:
                glBindBuffer(GL_ARRAY_BUFFER, buffer['faces.color'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer['faces'])
                glDrawElements(GL_TRIANGLES, buffer['f'], GL_UNSIGNED_INT, None)

                glBindBuffer(GL_ARRAY_BUFFER, buffer['faces.color:back'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer['faces:back'])
                glDrawElements(GL_TRIANGLES, buffer['f'], GL_UNSIGNED_INT, None)

            if self.settings['edges.on']:
                glLineWidth(self.settings['edges.width:value'])
                glBindBuffer(GL_ARRAY_BUFFER, buffer['edges.color'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer['edges'])
                glDrawElements(GL_LINES, buffer['e'], GL_UNSIGNED_INT, None)

            if self.settings['vertices.on']:
                glPointSize(self.settings['vertices.size:value'])
                glBindBuffer(GL_ARRAY_BUFFER, buffer['vertices.color'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer['vertices'])
                glDrawElements(GL_POINTS, buffer['v'], GL_UNSIGNED_INT, None)

            glDisableClientState(GL_COLOR_ARRAY)
            glDisableClientState(GL_VERTEX_ARRAY)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
