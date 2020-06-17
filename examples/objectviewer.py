from random import randint as rdi

from math import radians

from compas.geometry import Box
from compas.datastructures import Mesh
from compas.datastructures import mesh_transform_numpy
from compas.utilities import rgb_to_hex
from compas.geometry import Translation
from compas.geometry import Rotation

from compas_viewers.objectviewer import ObjectViewer


viewer = ObjectViewer()
# make 10 random meshes
# with random position and orientation
for i in range(10):
    T = Translation.from_vector([rdi(0, 10), rdi(0, 10), rdi(0, 5)])
    R = Rotation.from_axis_and_angle([0, 0, 1.0], radians(rdi(0, 180)))
    X = T * R
    box = Box.from_width_height_depth(rdi(1, 3), rdi(1, 3), rdi(1, 3))
    mesh = Mesh.from_shape(box)
    mesh_transform_numpy(mesh, X)

    viewer.add(mesh, name="Mesh.%s"%i, settings={
        'color': rgb_to_hex((rdi(0, 255), rdi(0, 255), rdi(0, 255))),
        'edges.width': 2,
        'opacity': 0.7,
        'vertices.size': 10,

        'vertices.on': True,
        'edges.on': False,
        'faces.on': True,
        })

viewer.show()
