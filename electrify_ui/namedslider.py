from PySide6 import QtWidgets
from PySide6.QtCore import Signal

from .qt_screens.ui_namedslider import Ui_NamedSlider


class NamedSlider(QtWidgets.QWidget, Ui_NamedSlider):
    valueChanged = Signal(int, float)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.setValue(0.5)
        self.sliderNameLabel.setText('')
        self.valueSlider.valueChanged.connect(self.onValueChanged)

    def configure(self, id, title, init_value=None):
        self.id = id
        self.setTitle(title)
        if init_value is not None:
            self.setValue(init_value)

    def setValue(self, value: float):
        self.valueSlider.setValue(value * 100.0)

    @property
    def value(self):
        return self.valueSlider.value

    def setTitle(self, title):
        self.sliderNameLabel.setText(title)

    def onValueChanged(self):
        value = self.valueSlider.value() / 100.0
        self.sliderValueLabel.setText('{:1.2f}'.format(value))
        self.valueChanged.emit(self.id, value)
