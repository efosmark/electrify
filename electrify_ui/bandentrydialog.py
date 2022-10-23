from .qt_screens.ui_bandentrydialog import Ui_BandEntryDialog
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Signal


class BandEntryDialog(QtWidgets.QDialog, Ui_BandEntryDialog):
    bandAccepted = Signal(float, float)

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent=parent)
        self.setupUi(self)

        self.dialogButtonBox.accepted.connect(self._onAccept)
        self.dialogButtonBox.rejected.connect(self.hide)
        self.validationLabel.setVisible(False)

    def _onAccept(self):
        self.validationLabel.setVisible(False)
        start = self.startFrequencyInput.getValue()
        end = self.endFrequencyInput.getValue()
        if end is None:
            self.validationLabel.setText('End frequency must be specified.')
            self.validationLabel.setVisible(True)
        elif end <= start:
            self.validationLabel.setText('End must be greater than start.')
            self.validationLabel.setVisible(True)
        else:
            self.bandAccepted.emit(start, end)
            self.hide()

    def display(self):
        self.validationLabel.setVisible(False)
        self.startFrequencyInput.setValue(0.0)
        self.endFrequencyInput.setValue(0.0)
        self.show()
        QtCore.QTimer.singleShot(10, self.startFrequencyInput.focusWidget)
