from OpenGL.GL import *  # noqa: F401 F403
from OpenGL.GLUT import *  # noqa: F401 F403
from OpenGL.GLU import *  # noqa: F401 F403

from PySide2.QtWidgets import QTreeWidget
from PySide2.QtWidgets import QTreeWidgetItem


class ObjectTree(QTreeWidget):

    def __init__(self):
        super().__init__()
        self.setColumnCount(1)
        items = []
        for i in range(10):
            items.append(QTreeWidgetItem(None, ["item: {}".format(i)]))
        self.insertTopLevelItems(None, items)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
