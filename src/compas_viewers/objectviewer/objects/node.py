from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import uuid


__all__ = ['Node']


class Node(object):
    """"""

    def __init__(self, settings={}):
        self.guid = uuid.uuid4()
        self.children = []
        self._settings = {}
        self._settings.update(settings)

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        return self._settings.update(settings)

    def add(self, node):
        if node not in self.children:
            self.children.append(node)

    def remove(self, node):
        self.children.remove(node)

    def traverse(self):
        flat_list = [self]
        for child_node in self.children:
            flat_list += child_node.traverse()
        return flat_list

# ==============================================================================
# Main
# ==============================================================================


if __name__ == '__main__':
    pass
