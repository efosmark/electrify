from PySide6 import QtWidgets
from PySide6.QtCore import Signal

from .qt_screens.ui_paginator import Ui_Paginator


class Paginator(QtWidgets.QWidget, Ui_Paginator):
    pageChanging = Signal(int, object)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.pages = []
        self.page_index = 0
        self.pageChanging.connect(self._pageChanging)

        self.nextButton.clicked.connect(self.onPageNext)
        self.prevButton.clicked.connect(self.onPagePrev)

        self.setStateLoading()

    def getCurrentPageModel(self):
        if 0 <= self.page_index < len(self.pages):
            return self.pages[self.page_index]

    def goToPage(self, page_id):
        if page_id >= 0 and page_id < len(self.pages):
            self.setStateLoading()
            self.pageChanging.emit(page_id, self.pages[page_id])

    def addPage(self, page):
        self.pages.append(page)
        return len(self.pages) - 1

    def onPageNext(self):
        return self.goToPage(self.page_index + 1)

    def onPagePrev(self):
        return self.goToPage(self.page_index - 1)

    def setStateLoading(self):
        self.nextButton.setEnabled(False)
        self.prevButton.setEnabled(False)

    def setStateLoaded(self):
        self.nextButton.setEnabled(self.page_index < len(self.pages) - 1)
        self.prevButton.setEnabled(self.page_index > 0)
        self.pageLabel.setText('{} / {}'.format(self.page_index + 1, len(self.pages)))

    def _pageChanging(self, page_id):
        self.setStateLoading()

    def pageChanged(self, page_id):
        self.page_index = page_id
        self.setStateLoaded()
