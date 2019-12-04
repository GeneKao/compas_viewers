# Mesh

# def func(self):
#     self.update_vertices_colors(colors={0: [255, 0, 0], 1: [0, 255, 0], 5: [0, 0, 255]})
#     print('Colour change!')

# data = {
#     'vertices': [
#         [-3, -3, 0],
#         [+3, -3, 0],
#         [+3, +3, 0],
#         [-3, +3, 0],
#         [-3, -3, 3],
#         [+3, -3, 3],
#         [+3, +3, 3],
#         [-3, +3, 3],
#     ],
#     # turn on vertex coloring by uncommenting
#     # 'vertex_colors': {
#     #     0: [255, 0, 255],
#     #     1: [255, 0, 0],
#     #     2: [255, 255, 0],
#     #     3: [255, 255, 0],
#     #     4: [0, 255, 0],
#     #     5: [0, 255, 150],
#     #     6: [0, 255, 255],
#     #     7: [0, 0, 255],
#     # },
#     'edges': [
#         {'vertices': [0, 4], 'color': [0, 0, 0]},
#         {'vertices': [1, 5], 'color': [0, 0, 255]},
#         {'vertices': [2, 6], 'color': [0, 255, 0]},
#         {'vertices': [3, 7]}
#     ],
#     'faces': [
#         {'vertices': [4, 5, 6], 'color': [250, 150, 150]},
#         {'vertices': [6, 7, 4], 'color': [150, 150, 250]},
#     ],
# }

# viewer = VtkViewer(data=data)
# viewer.keycallbacks['s'] = func
# viewer.setup()
# viewer.update_vertices_coordinates(coordinates={0: [-3, -3, -2], 3: [-3, +3, -2]})
# viewer.start()

# Voxels

# from numpy import linspace
# from numpy import meshgrid

# r       = linspace(-1, 1, 50)
# x, y, z = meshgrid(r, r, r)

# data = {'voxels': x + y + z}

# viewer = VtkViewer(data=data)
# viewer.setup()
# viewer.start()

# Datastructure

from compas.datastructures import Mesh

import compas

datastructure = Mesh.from_obj(compas.get('quadmesh.obj'))

viewer = VtkViewer(datastructure=datastructure)
viewer.setup()
viewer.start()
