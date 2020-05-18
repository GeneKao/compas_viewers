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
from compas.datastructures import Network
from compas_viewers.objectviewer import MeshObject
from compas_viewers.objectviewer import NetworkObject

from compas.geometry import Point
from compas.geometry import Line
from compas.geometry import Polyline
from compas.geometry import Plane
from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Polyhedron


from compas_viewers.objectviewer import PointObject
from compas_viewers.objectviewer import LineObject
from compas_viewers.objectviewer import PolylineObject
from compas_viewers.objectviewer import PlaneObject
from compas_viewers.objectviewer import CircleObject
from compas_viewers.objectviewer import ConeObject
from compas_viewers.objectviewer import PolyhedronObject
from compas_viewers.objectviewer import ArrowObject
from compas_viewers.objectviewer import Arrow

Scene.register(Mesh, MeshObject)
Scene.register(Network, NetworkObject)
Scene.register(Point, PointObject)
Scene.register(Line, LineObject)
Scene.register(Polyline, PolylineObject)
Scene.register(Plane, PlaneObject)
Scene.register(Circle, CircleObject)
Scene.register(Cone, ConeObject)
Scene.register(Polyhedron, PolyhedronObject)
Scene.register(Arrow, ArrowObject)


__all__ = [name for name in dir() if not name.startswith('_')]
