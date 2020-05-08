"""
********************************************************************************
compas_rv2.scene
********************************************************************************

.. currentmodule:: compas_rv2.scene


.. autosummary::
    :toctree: generated/
    :nosignatures:

    Scene

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .scene import Scene

from compas.datastructures import Mesh
from compas_viewers.objectviewer import MeshObject

from compas.geometry import Point
from compas.geometry import Line
from compas.geometry import Polyline
from compas.geometry import Plane
from compas.geometry import Circle


from compas_viewers.objectviewer import PointObject
from compas_viewers.objectviewer import LineObject
from compas_viewers.objectviewer import PolylineObject
from compas_viewers.objectviewer import PlaneObject
from compas_viewers.objectviewer import CircleObject

Scene.register(Mesh, MeshObject)
Scene.register(Point, PointObject)
Scene.register(Line, LineObject)
Scene.register(Polyline, PolylineObject)
Scene.register(Plane, PlaneObject)
Scene.register(Circle, CircleObject)


__all__ = [name for name in dir() if not name.startswith('_')]
