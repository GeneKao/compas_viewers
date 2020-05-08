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
    viewer.add(line, settings = {'color': rgb_to_hex((210, 210, 210))})


point = Point(0,0,0)
viewer.add(point, settings = {'color': rgb_to_hex((210, 210, 210))})


polyline = Polyline([[2,0,0], [1,0,0], [1,1,0], [1,1,1]])
viewer.add(polyline, settings = {'color': rgb_to_hex((210, 210, 210))})


plane = Plane([0, 0, 2], [1, 1, 1])
viewer.add(plane, settings = {'color': rgb_to_hex((210, 210, 210))})

circle = Circle( Plane([0, 0, 3], [1, 1, 1]), 1)
viewer.add(circle, settings = {'color': rgb_to_hex((210, 210, 210))})


viewer.update()
viewer.show()
