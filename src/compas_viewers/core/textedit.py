from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets


__all__ = ['TextEdit']


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


class TextEdit(object):

    def __init__(self, text, value, edit, **kwargs):
        self.layout = QtWidgets.QVBoxLayout()
        box = QtWidgets.QHBoxLayout()
        self.input = QtWidgets.QLineEdit()
        self.input.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.input.setFrame(False)
        # self.input.setFixedWidth(kwargs.get('edit.width'))
        # self.input.setFixedHeight(kwargs.get('edit.height'))
        if value:
            self.input.setText(str(value))
        box.addWidget(self.input)
        if text:
            label = QtWidgets.QLabel()
            label.setText(text)
            box.addWidget(label)
        # box.addStretch()
        self.input.setTextMargins(2, 0, 2, 0)
        self.input.editingFinished.connect(self.edit(edit))
        self.layout.addLayout(box)
        # self.layout.addStretch()

    def edit(self, f):
        def wrapper():
            text = self.input.text()
            if text:
                value = float(text)
                f(value)
        return wrapper


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
