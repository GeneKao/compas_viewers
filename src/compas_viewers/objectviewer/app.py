from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from compas_viewers.core import App

from compas_viewers.objectviewer import MeshObject
from compas_viewers.objectviewer.view import View
from compas_viewers.objectviewer.controller import Controller

from compas_viewers.objectviewer.settings import SETTINGS
from compas_viewers.objectviewer.ui import UI
from compas_viewers.objectviewer.style import STYLE
from compas_viewers.objectviewer.PyQtJsonModel import QJsonModel
import json

__all__ = ['ObjectViewer']


class ObjectTree(QtWidgets.QTreeWidget):

    def __init__(self):
        super().__init__()
        self.setColumnCount(1)
        self.setHeaderLabels(['Scene'])


class Manager(object):

    def __init__(self, parent, app):
        self._items = []
        self.app = app
        self.parent = parent
        self.widget = ObjectTree()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.widget.setLayout(self.layout)
        self.parent.setWidget(self.widget)
        self.widget.itemSelectionChanged.connect(self.on_item_selection_changed)
        self.widget.itemDoubleClicked.connect(self.on_item_double_clicked)

    def set_items(self, nodes):

        # clean up first
        while self.widget.topLevelItemCount()>0:
            self.widget.takeTopLevelItem(0)

        self._items = nodes
        top_items = [self._add_node_item(node, parent=None) for node in nodes]
        self.widget.addTopLevelItems(top_items)

    def _add_node_item(self, node, parent=None):
        if parent:
            nodeitem = QtWidgets.QTreeWidgetItem(parent)
        else:
            nodeitem = QtWidgets.QTreeWidgetItem()
        nodeitem.setText(0, node.name)
        node.widget = nodeitem
        
        for child_node in node.children:
            self._add_node_item(child_node, nodeitem)

        return nodeitem

    def find_selected_item(self, item):
        index = self.widget.indexFromItem(item)
        trail = []
        while True:
            i = index.row()
            j = index.column()
            if i == -1 and j == -1:
                break
            trail.append((i, j))
            index = index.parent()
        return trail[::-1]

    def find_item_node(self, item):
        trail = self.find_selected_item(item)
        mid = trail[0][0]
        node = self._items[mid]
        return node

    def on_item_selection_changed(self):
        for item in self.widget.selectedItems():
            node = self.find_item_node(item)
            if node not in self.app.view.selected:
                self.app.view.selected.add(node)

        self.app.view.updateGL()

    def on_item_double_clicked(self, item):
        node = self.find_item_node(item)
        p = ObjectProperty(self.parent, data=node.to_data())
        p.show()

class ObjectProperty(QtWidgets.QDialog):
    def __init__(self, parent=None, data={}):
        super(ObjectProperty, self).__init__(parent)
        self.resize(500, 800)
        self.setWindowTitle("Property")

        # conver data dict to json format
        json_data = json.dumps(data)
        json_data = json.loads(json_data)

        model = QJsonModel(json_data = json_data)
        view = QtWidgets.QTreeView()
        view.setModel(model)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(view)
        self.setLayout(layout)
        

class ObjectViewer(App):
    """"""

    def __init__(self, grid=True, axis=True, activate_selection=False):
        super().__init__(SETTINGS, UI, STYLE)

        self.activate_selection = activate_selection
        self.controller = Controller(self)
        self.view = View(self.controller, activate_selection)
        # self.view.camera.events.rotX.connect(self.controller.on_rotX)
        # self.view.camera.events.rotZ.connect(self.controller.on_rotZ)
        # self.view.camera.events.distance.connect(self.controller.on_distance)

        self.setup()
        self.init()

        if self.activate_selection:
            self.init_sidebar2()
            self.manager = Manager(self.sidebar2, self)

        self.view.glInit()
        if grid:
            self.view.setup_grid()
        if axis:
            self.view.setup_axes()
        self.view.setFocus()

    def init_sidebar2(self):
        self.sidebar2 = QtWidgets.QDockWidget()
        self.sidebar2.setObjectName('Sidebar')
        self.sidebar2.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.sidebar2.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.sidebar2.setMinimumWidth(180)
        self.sidebar2.setTitleBarWidget(QtWidgets.QWidget())
        self.sidebar2.setContentsMargins(0, 0, 0, 0)
        self.main.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.sidebar2)

    @property
    def scene(self):
        # TODO: Where is it optimal to put scene ??
        return self.controller.scene

    @scene.setter
    def scene(self, scene):
        self.controller.scene = scene
        # self.controller.center()
        self.update()

    def add(self, mesh, *args, **kwargs):
        self.scene.add(mesh, *args, **kwargs)
        # self._update_items()

    def update(self):
        if self.activate_selection:
            self.manager.set_items(list(self.controller.scene.traverse(recursive=False)))
        self.view.glInit()
        self.view.make_buffers()
        self.view.updateGL()

    def show(self):
        self.update()
        super(ObjectViewer, self).show()

# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
