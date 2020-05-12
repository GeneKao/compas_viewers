from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import numpy as np

class Arrow(object):
    def __init__(self, point, direction):
        self.point = np.array(point)
        self.direction = np.array(direction)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass