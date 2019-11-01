import compas
from compas.datastructures import Mesh
from compas_viewers import MeshViewer


viewer = MeshViewer()
viewer.mesh = Mesh.from_polyhedron(6)

viewer.show()
