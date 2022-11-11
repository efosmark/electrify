
from typing import OrderedDict
from PySide6 import QtWidgets
from .qt_screens.ui_frequencyentry import Ui_FrequencyEntry
import logging
from electrify.util import logfunc

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

MAGNITUDES = OrderedDict({
    'Hz': 1,
    'kHz': 1e3,
    'MHz': 1e6,
    'GHz': 1e9
})


class FrequencyEntry(QtWidgets.QWidget, Ui_FrequencyEntry):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.setupUi(self)

    @logfunc(logger)
    def getValue(self):
        start = self.frequencyInput.value()
        startMag = MAGNITUDES[self.magnitudeInput.currentText()]
        return float(start * startMag)

    def clear(self):
        self.frequencyInput.setValue(0.0)

    def setValue(self, frequency: float):
        if frequency > 1e9:  # G
            self.frequencyInput.setValue(frequency/float(1e9))
            self.magnitudeInput.setCurrentIndex(list(MAGNITUDES.values()).index(1e9))
        elif frequency > 1e6:  # M
            self.frequencyInput.setValue(frequency/float(1e6))
            self.magnitudeInput.setCurrentIndex(list(MAGNITUDES.values()).index(1e6))
        elif frequency > 1e3:  # k
            self.frequencyInput.setValue(frequency/float(1e3))
            self.magnitudeInput.setCurrentIndex(list(MAGNITUDES.values()).index(1e3))
        else:
            self.frequencyInput.setValue(frequency)
            self.magnitudeInput.setCurrentIndex(0)
