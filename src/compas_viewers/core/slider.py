from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial
from decimal import Decimal

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets


__all__ = ['Slider']


class Validator(QtGui.QValidator):
    def __init__(self, minval, maxval):
        super(Validator, self).__init__()
        self.minval = int(minval)
        self.maxval = int(maxval)

    def validate(self, text, someint):
        try:
            int(text)
        except ValueError:
            return QtWidgets.QValidator.Invalid
        else:
            return QtWidgets.QValidator.Acceptable
            # if int(text) >= self.minval and int(text) <= self.maxval:
            # else:
            #     return QtWidgets.QValidator.Intermediate
        return QtWidgets.QValidator.Invalid


class Slider(object):

    # [0] text
    # -------|------------

    def __init__(self, name, text, value, minval, maxval, step, scale, slide, edit, **kwargs):
        self.name = name
        self.scale = scale
        self.precision = scale
        self.layout = QtWidgets.QVBoxLayout()
        box1 = QtWidgets.QHBoxLayout()
        box2 = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel()
        label.setText(text)
        self.input = QtWidgets.QLineEdit()
        self.input.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.input.setFrame(False)
        self.input.setFixedWidth(kwargs.get('edit.width', 48))
        self.input.setFixedHeight(kwargs.get('edit.width', 24))
        self.input.setText(str(value))
        # box1.addWidget(self.input)
        box1.addWidget(label)
        box1.addStretch()
        self.input.setTextMargins(2, 0, 2, 0)
        # edit.setValidator(Validator(minval, maxval))
        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setMinimum(minval)
        self.slider.setMaximum(maxval)
        self.slider.setSingleStep(step)
        self.slider.setValue(int(value / scale))
        self.slider.setTracking(True)
        self.slider.valueChanged.connect(self.slide(slide))
        self.input.textEdited.connect(self.edit(edit))
        box2.addWidget(self.input)
        box2.addWidget(self.slider)
        self.layout.addLayout(box1)
        self.layout.addLayout(box2)
        self.layout.addStretch()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = max(self.slider.minimum(), min(value, self.slider.maximum()))

    @property
    def precision(self):
        return self._precision

    @precision.setter
    def precision(self, scale):
        d = Decimal(str(scale)).as_tuple()
        if d.exponent < 0:
            e = - d.exponent
            p = "{}f".format(e)
        else:
            e = 0
            p = "{}f".format(e)
        self._precision = p

    def slide(self, f):
        def wrapper(position):
            self.value = position * self.scale
            self.input.setText("{0:.{1}}".format(self.value, self.precision))
            f(self.value)
        return wrapper

    def edit(self, f):
        def wrapper(text):
            if text:
                self.value = int(float(text) / self.scale)
                self.slider.setValue(self.value)
                f(float(self.value) * self.scale)
        return wrapper


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
