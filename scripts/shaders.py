import sys

import numpy as np
import ctypes

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from OpenGL.GL import *
from OpenGL.GLUT import *

from numpy import array
from numpy import float64
from numpy import int32


# //uniform mat4 view;
# //uniform mat4 model;
# //uniform mat4 projection;

# //gl_Position = projection * view * model * vec4(position, 1.0);


class View(QtWidgets.QOpenGLWidget):

    vertexcode = """
attribute vec3 a_position;
attribute vec4 a_color;
uniform vec4 u_color;
varying vec4 v_color;

void main()
{
    v_color = u_color * a_color;
    gl_Position = vec4(a_position, 1.0);
}
"""

    fragmentcode = """
varying vec4 v_color;

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
            [0.0, 1.0, 0.0]], dtype=np.float64)
        self.colors = np.array([
            [1.0, 0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0, 1.0],
            [0.0, 1.0, 1.0, 1.0],
            [0.0, 0.0, 1.0, 1.0]], dtype=np.float64)
        self.vertices = np.array([0, 1, 2], dtype=np.int32).flatten()
        self.faces = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.int32).flatten()
        self.edges = np.array([[0, 1], [1, 2], [2, 0], [2, 3], [3, 0]], dtype=np.int32).flatten()
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

    def make_vertex_buffers(self):
        # vertex locations
        data = self.xyz
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
        self.buffers['xyz'] = buffer
        # vertex colors
        data = self.colors
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
        self.buffers['colors'] = buffer

    def make_element_buffers(self):
        # faces
        data = self.faces
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
        self.buffers['faces'] = buffer
        # edges
        data = self.edges
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
        self.buffers['edges'] = buffer

    def set_attributes(self):
        # position
        loc = glGetAttribLocation(self.program, "a_position")
        size = self.xyz.shape[1]
        stride = self.xyz.strides[0]
        offset = ctypes.c_void_p(0)
        glEnableVertexAttribArray(loc)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffers['xyz'])
        glVertexAttribPointer(loc, size, GL_DOUBLE, False, stride, offset)
        # color
        loc = glGetAttribLocation(self.program, "a_color")
        size = self.colors.shape[1]
        stride = self.colors.strides[0]
        offset = ctypes.c_void_p(0)
        glEnableVertexAttribArray(loc)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffers['colors'])
        glVertexAttribPointer(loc, size, GL_DOUBLE, False, stride, offset)
        # uniform color
        loc = glGetUniformLocation(self.program, "u_color")
        glUniform4f(loc, 1, 1, 1, 1)

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
        self.set_attributes()

    def paintGL(self):
        context = self.context()
        f = context.functions()
        if not self.isValid():
            return
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            return
        # faces
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
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
        glDrawElements(GL_LINES, self.edges.size, GL_UNSIGNED_INT, None)
        glDepthMask(GL_TRUE)

    def resizeEvent(self, event):
        context = self.context()
        if context:
            f = context.functions()
            w = event.size().width()
            h = event.size().height()
            glViewport(0, 0, w, h)

    def resizGL(self, w, h):
        context = self.context()
        f = context.functions()
        glViewport(0, 0, w, h)


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
