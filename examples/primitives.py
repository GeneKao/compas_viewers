import random

from compas.utilities import rgb_to_hex
from compas.geometry import Point
from compas.geometry import Line
from compas.geometry import Polyline
from compas.geometry import Plane
from compas.geometry import Circle

from compas_viewers.objectviewer import ObjectViewer

viewer = ObjectViewer()

for i in range(10):
    line = Line(
        Point(random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 10)),
        Point(random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 10))
    )
    viewer.add(line)


point = Point(0,0,0)
viewer.add(point)


polyline = Polyline([[2,0,0], [1,0,0], [1,1,0], [1,1,1]])
viewer.add(polyline)


plane = Plane([0, 0, 2], [1, 1, 1])
viewer.add(plane)

circle = Circle( Plane([0, 0, 3], [1, 1, 1]), 1)
viewer.add(circle)


viewer.update()
viewer.show()
