import sys

from math import tan
from math import pi
from math import radians

import numpy as np
import ctypes

from glumpy import gloo
from glumpy import glm

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from OpenGL.GL import *
from OpenGL.GLUT import *

from numpy import array
from numpy import float64
from numpy import int32

from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import Scale
from compas.geometry import Projection


class View(QtWidgets.QOpenGLWidget):

    vertexcode = """
uniform mat4   model;
uniform mat4   view;
uniform mat4   projection;

attribute vec3 a_position;
attribute vec4 a_color;

uniform vec4   u_color;

varying vec4 v_color; // out

void main()
{
    v_color = u_color * a_color;
    gl_Position = projection * view * model * vec4(a_position, 1.0);
}
"""

    fragmentcode = """
varying vec4 v_color; // in

void main()
{
    gl_FragColor = v_color;
}
"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.program = None
        self.xyz = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 1.0],
            [1.0, 1.0, 1.0],
            [0.0, 1.0, 1.0]], dtype=np.float32)
        self.colors = np.array([
            [1.0, 0.0, 0.0, 1.0],
            [1.0, 1.0, 0.0, 1.0],
            [0.0, 1.0, 0.0, 1.0],
            [0.0, 1.0, 1.0, 1.0],
            [0.0, 0.0, 1.0, 1.0],
            [0.0, 1.0, 1.0, 1.0],
            [0.0, 1.0, 0.0, 1.0],
            [1.0, 1.0, 0.0, 1.0]], dtype=np.float32)
        self.vertices = np.array([0, 1, 2, 3, 4, 5, 6, 7], dtype=np.int32)
        self.faces = np.array([
            [0, 2, 1], [0, 3, 2],
            [0, 1, 5], [0, 5, 4],
            [4, 3, 0], [4, 7, 3],
            [7, 2, 3], [7, 6, 2],
            [6, 5, 2], [5, 1, 2],
            [4, 6, 7], [5, 6, 4]], dtype=np.int32).flatten()
        self.edges = np.array([[0, 1], [1, 2], [2, 0], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]], dtype=np.int32).flatten()
        self.buffers = {'xyz': None, 'vertices': None, 'edges': None, 'faces': None, 'colors': None}

    def make_shader_program(self):
        context = self.context()
        f = context.functions()

        program = glCreateProgram()
        vertex = glCreateShader(GL_VERTEX_SHADER)
        fragment = glCreateShader(GL_FRAGMENT_SHADER)

        glShaderSource(vertex, self.vertexcode)
        glShaderSource(fragment, self.fragmentcode)

        glCompileShader(vertex)
        if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(vertex).decode()
            raise RuntimeError("Vertex shader compilation error: {}".format(error))

        glCompileShader(fragment)
        if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(fragment).decode()
            raise RuntimeError("Fragment shader compilation error: {}".format(error))

        glAttachShader(program, vertex)
        glAttachShader(program, fragment)

        glLinkProgram(program)
        if not glGetProgramiv(program, GL_LINK_STATUS):
            error = glGetProgramInfoLog(program).decode()
            raise RuntimeError("Linking error: {}".format(error))

        glDetachShader(program, vertex)
        glDetachShader(program, fragment)

        glUseProgram(program)

        self.program = program

    def make_vertex_buffer(self, data):
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
        return buffer

    def make_vertex_buffers(self):
        self.buffers['xyz'] = self.make_vertex_buffer(self.xyz)
        self.buffers['colors'] = self.make_vertex_buffer(self.colors)

    def make_element_buffer(self, data):
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
        return buffer

    def make_element_buffers(self):
        self.buffers['faces'] = self.make_element_buffer(self.faces)
        self.buffers['edges'] = self.make_element_buffer(self.edges)
        self.buffers['vertices'] = self.make_element_buffer(self.vertices)

    def set_position_attribute(self):
        loc = glGetAttribLocation(self.program, "a_position")
        size = self.xyz.shape[1]
        stride = self.xyz.strides[0]
        offset = ctypes.c_void_p(0)
        glEnableVertexAttribArray(loc)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffers['xyz'])
        glVertexAttribPointer(loc, size, GL_FLOAT, False, stride, offset)

    def set_color_attribute(self):
        loc = glGetAttribLocation(self.program, "a_color")
        size = self.colors.shape[1]
        stride = self.colors.strides[0]
        offset = ctypes.c_void_p(0)
        glEnableVertexAttribArray(loc)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffers['colors'])
        glVertexAttribPointer(loc, size, GL_FLOAT, False, stride, offset)

    def set_uniform_color(self):
        loc = glGetUniformLocation(self.program, "u_color")
        glUniform4f(loc, 1, 1, 1, 1)

    def set_model_matrix(self):
        I = np.eye(4, dtype=np.float32)
        loc = glGetUniformLocation(self.program, "model")
        glUniformMatrix4fv(loc, 1, False, I)

    def set_view_matrix(self):
        T = np.array(Translation([0, 0, -5]), dtype=np.float32)
        Rx = np.array(Rotation.from_axis_and_angle([1.0, 0.0, 0.0], radians(-60)), dtype=np.float32)
        Rz = np.array(Rotation.from_axis_and_angle([0.0, 0.0, 1.0], radians(30)), dtype=np.float32)
        loc = glGetUniformLocation(self.program, "view")
        glUniformMatrix4fv(loc, 1, True, T.dot(Rx.dot(Rz)))

    def set_projection_matrix(self):
        w = self.width()
        h = self.height()
        P = glm.perspective(45.0, w / float(h), 0.1, 100.0)
        loc = glGetUniformLocation(self.program, "projection")
        glUniformMatrix4fv(loc, 1, False, P)

    def initializeGL(self):
        context = self.context()
        f = context.functions()

        # init
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glClearColor(255, 255, 255, 255)
        glCullFace(GL_BACK)
        glShadeModel(GL_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glPolygonOffset(1.0, 1.0)
        glEnable(GL_POLYGON_OFFSET_FILL)
        glEnable(GL_CULL_FACE)
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

        # further init
        self.make_shader_program()
        self.make_vertex_buffers()
        self.make_element_buffers()
        self.set_position_attribute()
        self.set_color_attribute()
        self.set_uniform_color()
        self.set_model_matrix()
        self.set_view_matrix()
        self.set_projection_matrix()

    def paintGL(self):
        context = self.context()
        f = context.functions()

        if not self.isValid():
            return
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # faces
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.buffers['faces'])
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_POLYGON_OFFSET_FILL)
        loc = glGetUniformLocation(self.program, "u_color")
        glUniform4f(loc, 1, 1, 1, 1)
        glDrawElements(GL_TRIANGLES, self.faces.size, GL_UNSIGNED_INT, None)

        # edges
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.buffers['edges'])
        glDisable(GL_POLYGON_OFFSET_FILL)
        glEnable(GL_BLEND)
        glDepthMask(GL_FALSE)
        loc = glGetUniformLocation(self.program, "u_color")
        glUniform4f(loc, 0, 0, 0, 1)
        glLineWidth(3.0)
        glDrawElements(GL_LINES, self.edges.size, GL_UNSIGNED_INT, None)
        glDepthMask(GL_TRUE)

    def resizeGL(self, w, h):
        context = self.context()
        f = context.functions()

        glViewport(0, 0, w, h)

        self.set_projection_matrix()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = QtWidgets.QMainWindow()
    view = View()

    main.setCentralWidget(view)
    main.resize(1440, 900)
    main.show()

    sys.exit(app.exec_())
