"""
compas_viewers.core
===================

.. currentmodule:: compas_viewers.core

Classes
-------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    App
    Arrow
    Axes
    Camera
    ColorButton
    Controller
    GLWidget
    Grid
    Mouse
    QColorButton
    Slider
    TextEdit

Functions
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    draw_points
    draw_lines
    draw_faces
    draw_sphere
    draw_points
    draw_lines
    draw_polygons
    draw_cylinders
    draw_spheres
    draw_texts

    make_vertex_buffer
    make_index_buffer

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .drawing import *
from .arrow import *
from .axes import *
from .camera import *
from .grid import *
from .mouse import *
from .slider import *
from .colorbutton import *
from .glwidget import *
from .openglwidget import *
from .controller import *
from .textedit import *
from .buffers import *

from .app import *

__all__ = [name for name in dir() if not name.startswith('_')]
