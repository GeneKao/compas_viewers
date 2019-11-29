from OpenGL.GL import *  # noqa: F401 F403
from OpenGL.GLUT import *  # noqa: F401 F403
from OpenGL.GLU import *  # noqa: F401 F403


__all__ = [
    'make_vertex_buffer',
    'make_index_buffer'
]


def make_vertex_buffer(data, dynamic=False):
    d = len(data)
    b = glGenBuffers(1)
    cdata = (ctypes.c_float * d)(* data)
    usage = GL_DYNAMIC_DRAW if dynamic else GL_STATIC_DRAW
    glBindBuffer(GL_ARRAY_BUFFER, b)
    glBufferData(GL_ARRAY_BUFFER, 4 * d, cdata, usage)
    return b


def make_index_buffer(indices, dynamic=False):
    i = len(indices)
    b = glGenBuffers(1)
    cindices = (ctypes.c_uint * i)(* indices)
    usage = GL_DYNAMIC_DRAW if dynamic else GL_STATIC_DRAW
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, b)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * i, cindices, usage)
    return b


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
