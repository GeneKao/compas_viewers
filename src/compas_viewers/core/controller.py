from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtOpenGL
from PySide2 import QtWidgets
from PySide2.QtOpenGL import QGLWidget as QOpenGLWidget

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


__all__ = ['Controller']


class Controller(object):

    settings = {}

    def __init__(self, app):
        self.app = app
        self.controls = {}

    @property
    def view(self):
        return self.app.view

    def message(self, text):
        box = QtWidgets.QMessageBox(parent=self.app.main)
        box.setText(text)
        box.show()

    def debug(self, source, mtype, mid, severity, length, raw, user):
        text = [
            "OpenGL Debug Info",
            "================="
            "source: {}".format(source),
            "message type: {}".format(mtype),
            "message id: {}".format(mid),
            "severity: {}".format(severity),
            "user: {}".format(user),
            "",
            "{}".format(raw[:length])
        ]
        self.log("\n".join(text))

    def log(self, text):
        # self.app.console.findChild(QtWidgets.QPlainTextEdit).appendPlainText(text)
        self.app.console.widget().appendPlainText(text)

    def opengl_version_info(self):
        context = self.app.view.context()
        functions = context.functions()
        text = [
            "Vendor: {}".format(functions.glGetString(GL_VENDOR)),
            "Renderer: {}".format(functions.glGetString(GL_RENDERER)),
            "GL Version: {}".format(functions.glGetString(GL_VERSION)),
            "GLSL Version: {}".format(functions.glGetString(GL_SHADING_LANGUAGE_VERSION)),
        ]
        self.message('\n'.join([str(line) for line in text]))

    def opengl_extensions(self):
        extensions = str(glGetString(GL_EXTENSIONS)).split(' ')
        for name in extensions:
            print(name)

    def opengl_set_version(self, version):
        major, minor = version
        gl_format = QtOpenGL.QGLFormat()
        gl_format.setVersion(major, minor)
        gl_format.setProfile(QtOpenGL.QGLFormat.CoreProfile)
        gl_format.setSampleBuffers(True)
        # gl_format.setDefaultFormat(gl_format)
        self.view.context().setFormat(gl_format)
        self.view.context().create()
        self.view.glInit()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
