# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bandselect.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_BandSelect(object):
    def setupUi(self, BandSelect):
        if not BandSelect.objectName():
            BandSelect.setObjectName(u"BandSelect")
        BandSelect.resize(244, 114)
        self.horizontalLayout = QHBoxLayout(BandSelect)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.bandTableWidget = QTableWidget(BandSelect)
        if (self.bandTableWidget.columnCount() < 2):
            self.bandTableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setText(u"Start");
        self.bandTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        font = QFont()
        font.setFamilies([u"Ubuntu"])
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setText(u"End");
        __qtablewidgetitem1.setFont(font);
        self.bandTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.bandTableWidget.rowCount() < 2):
            self.bandTableWidget.setRowCount(2)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.bandTableWidget.setVerticalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.bandTableWidget.setVerticalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.bandTableWidget.setItem(0, 0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.bandTableWidget.setItem(0, 1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.bandTableWidget.setItem(1, 0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.bandTableWidget.setItem(1, 1, __qtablewidgetitem7)
        self.bandTableWidget.setObjectName(u"bandTableWidget")
        self.bandTableWidget.setMinimumSize(QSize(200, 0))
        self.bandTableWidget.setMaximumSize(QSize(200, 16777215))
        self.bandTableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.bandTableWidget.setProperty("showDropIndicator", False)
        self.bandTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.bandTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.bandTableWidget.setWordWrap(False)
        self.bandTableWidget.setCornerButtonEnabled(False)
        self.bandTableWidget.horizontalHeader().setMinimumSectionSize(50)
        self.bandTableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.bandTableWidget.verticalHeader().setVisible(False)

        self.horizontalLayout.addWidget(self.bandTableWidget)

        self.widget = QWidget(BandSelect)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(35, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.addBandButton = QPushButton(self.widget)
        self.addBandButton.setObjectName(u"addBandButton")

        self.verticalLayout_2.addWidget(self.addBandButton)

        self.removeBandButton = QPushButton(self.widget)
        self.removeBandButton.setObjectName(u"removeBandButton")
        self.removeBandButton.setEnabled(False)

        self.verticalLayout_2.addWidget(self.removeBandButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(BandSelect)

        QMetaObject.connectSlotsByName(BandSelect)
    # setupUi

    def retranslateUi(self, BandSelect):
        BandSelect.setWindowTitle(QCoreApplication.translate("BandSelect", u"Form", None))
        ___qtablewidgetitem = self.bandTableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("BandSelect", u"New Row", None));
        ___qtablewidgetitem1 = self.bandTableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("BandSelect", u"New Row", None));

        __sortingEnabled = self.bandTableWidget.isSortingEnabled()
        self.bandTableWidget.setSortingEnabled(False)
        ___qtablewidgetitem2 = self.bandTableWidget.item(0, 0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("BandSelect", u"123", None));
        ___qtablewidgetitem3 = self.bandTableWidget.item(0, 1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("BandSelect", u"345", None));
        ___qtablewidgetitem4 = self.bandTableWidget.item(1, 0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("BandSelect", u"545 kHz", None));
        ___qtablewidgetitem5 = self.bandTableWidget.item(1, 1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("BandSelect", u"6565 MHz", None));
        self.bandTableWidget.setSortingEnabled(__sortingEnabled)

        self.addBandButton.setText(QCoreApplication.translate("BandSelect", u"+", None))
        self.removeBandButton.setText(QCoreApplication.translate("BandSelect", u"del", None))
    # retranslateUi

