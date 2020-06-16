import random

from compas.geometry import Plane
from compas.geometry import Circle
from compas.geometry import Cone
from compas.geometry import Polyhedron
from compas_viewers.objectviewer import Arrow


from compas_viewers.objectviewer import ObjectViewer

viewer = ObjectViewer()

plane = Plane([2, 0, 0], [0, 0, 1])
circle = Circle(plane, 0.5)
cone = Cone(circle, 1)
viewer.add(cone)

polyhedron = Polyhedron(4)
viewer.add(polyhedron)

arrow = Arrow([-2, 0, 0], [0, 1, 1])
viewer.add(arrow)

viewer.show()
