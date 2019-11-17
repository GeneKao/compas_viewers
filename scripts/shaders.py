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


class View(QtWidgets.QOpenGLWidget):

    vertexcode = """
attribute vec3 position;

void main()
{
    gl_Position = vec4(position, 1.0);
}
"""

    fragmentcode = """
uniform vec4 color;

void main()
{
    gl_FragColor = color;
}
"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.vertices = np.array([
            [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 1.0, 0.0], [0.0, 0.0, 0.0]
        ], dtype=np.float64)
        self.buffers = {'xyz': None, 'vertices': None, 'edges': None, 'faces': None}

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
            print(error)
            raise RuntimeError("Vertex shader compilation error.")

        glCompileShader(fragment)
        if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(fragment).decode()
            print(error)
            raise RuntimeError("Fragment shader compilation error.")

        glAttachShader(program, vertex)
        glAttachShader(program, fragment)

        glLinkProgram(program)
        if not glGetProgramiv(program, GL_LINK_STATUS):
            print(glGetProgramInfoLog(program))
            raise RuntimeError("Linking error.")

        glDetachShader(program, vertex)
        glDetachShader(program, fragment)

        glUseProgram(program)

        # xyz buffer
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        self.buffers['xyz'] = buffer

        # position attribute
        stride = self.vertices.strides[0]
        offset = ctypes.c_void_p(0)
        loc = glGetAttribLocation(program, "position")
        glEnableVertexAttribArray(loc)
        glVertexAttribPointer(loc, 3, GL_DOUBLE, False, stride, offset)

        # color attribute
        loc = glGetUniformLocation(program, "color")
        glUniform4f(loc, 0.0, 0.0, 1.0, 1.0)

    def initializeGL(self):
        context = self.context()
        f = context.functions()

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

        self.make_shader_program()

    def paintGL(self):
        context = self.context()
        f = context.functions()

        if not self.isValid():
            return
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, self.vertices.shape[0])

    def resizGL(self):
        context = self.context()
        f = context.functions()

        glViewport(0, 0, 1440, 900)


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
