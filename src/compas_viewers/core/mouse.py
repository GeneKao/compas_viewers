from PySide2 import QtCore


__all__ = ['Mouse']


class Mouse(object):
    """"""

    def __init__(self, view):
        self.view = view
        self.pos = QtCore.QPoint()
        self.last_pos = QtCore.QPoint()
        self.buttons = {'left': False, 'right': False}

    def dx(self):
        return self.pos.x() - self.last_pos.x()

    def dy(self):
        return self.pos.y() - self.last_pos.y()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
