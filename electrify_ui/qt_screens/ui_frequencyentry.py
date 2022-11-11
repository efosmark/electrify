# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frequencyentry.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QHBoxLayout,
    QSizePolicy, QWidget)

class Ui_FrequencyEntry(object):
    def setupUi(self, FrequencyEntry):
        if not FrequencyEntry.objectName():
            FrequencyEntry.setObjectName(u"FrequencyEntry")
        FrequencyEntry.resize(175, 35)
        FrequencyEntry.setMinimumSize(QSize(175, 35))
        FrequencyEntry.setMaximumSize(QSize(175, 35))
        self.horizontalLayout = QHBoxLayout(FrequencyEntry)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.frequencyInput = QDoubleSpinBox(FrequencyEntry)
        self.frequencyInput.setObjectName(u"frequencyInput")

        self.horizontalLayout.addWidget(self.frequencyInput)

        self.magnitudeInput = QComboBox(FrequencyEntry)
        self.magnitudeInput.addItem(u"Hz")
        self.magnitudeInput.addItem(u"kHz")
        self.magnitudeInput.addItem(u"MHz")
        self.magnitudeInput.addItem(u"GHz")
        self.magnitudeInput.setObjectName(u"magnitudeInput")
        self.magnitudeInput.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.magnitudeInput)


        self.retranslateUi(FrequencyEntry)

        QMetaObject.connectSlotsByName(FrequencyEntry)
    # setupUi

    def retranslateUi(self, FrequencyEntry):

        pass
    # retranslateUi

