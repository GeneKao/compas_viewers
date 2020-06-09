import random

from compas.utilities import rgb_to_hex
from compas.geometry import Point
from compas.geometry import Line
from compas.geometry import Polyline
from compas.geometry import Plane
from compas.geometry import Circle

from compas_viewers.objectviewer import ObjectViewer

viewer = ObjectViewer()


for j in range(1):

    pts = []
    for i in range(10):
        pts.append([random.uniform(0,10),random.uniform(0,10),random.uniform(0,10)]) 

    polyline = Polyline(pts)
    viewer.add(polyline,settings={"edges.color": "#ff0000", "edges.width":10})

pts = []
for i in range(10):
    pts.append([random.uniform(0,10),random.uniform(0,10),random.uniform(0,10)]) 

polyline = Polyline(pts)
viewer.add(polyline,settings={"edges.color": "#ff00ff"})


viewer.update()
viewer.show()
