from PySide6 import QtWidgets
from .qt_screens.ui_bandselect import Ui_BandSelect
from .bandentrydialog import BandEntryDialog

import logging
from electrify.util import logfunc

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BandSelect(QtWidgets.QWidget, Ui_BandSelect):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.bandEntryDialog = BandEntryDialog(self)
        self.bandEntryDialog.bandAccepted.connect(self.addBand)
        self.addBandButton.clicked.connect(self.bandEntryDialog.display)
        self.removeBandButton.clicked.connect(self._onRemoveBands)

        self.bandTableWidget.itemSelectionChanged.connect(self._onItemSelectionChanged)
        self.bands = []

    @logfunc(logger)
    def addBand(self, start, end):
        # band = (start, end)
        # if band not in self.bands:
        #     self.bandList.addItem('{} - {}'.format(
        #         e.format_value(start, unit='Hz', places=2),
        #         e.format_value(end, unit='Hz', places=2),
        #     ))
        self.removeBandButton.setEnabled(False)
        self.bandTableWidget.clearSelection()

    @logfunc(logger)
    def _onRemoveBands(self):
        for itm in self.bandTableWidget.selectedItems():
            idx = self.bandTableWidget.indexFromItem(itm).row()
            self.bandTableWidget.takeItem(idx)
            del self.bands[idx]
        self.removeBandButton.setEnabled(False)
        self.bandTableWidget.clearSelection()

    def _onItemSelectionChanged(self):
        self.removeBandButton.setEnabled(len(self.bandTableWidget.selectedItems()) > 0)
