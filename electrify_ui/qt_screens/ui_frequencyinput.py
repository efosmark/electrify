# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frequencyinput.ui'
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

class Ui_FrequencyInput(object):
    def setupUi(self, FrequencyInput):
        if not FrequencyInput.objectName():
            FrequencyInput.setObjectName(u"FrequencyInput")
        FrequencyInput.resize(161, 32)
        self.horizontalLayout = QHBoxLayout(FrequencyInput)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.frequencyInput = QDoubleSpinBox(FrequencyInput)
        self.frequencyInput.setObjectName(u"frequencyInput")

        self.horizontalLayout.addWidget(self.frequencyInput)

        self.magnitudeInput = QComboBox(FrequencyInput)
        self.magnitudeInput.addItem(u"Hz")
        self.magnitudeInput.addItem(u"kHz")
        self.magnitudeInput.addItem(u"MHZ")
        self.magnitudeInput.addItem(u"GHZ")
        self.magnitudeInput.setObjectName(u"magnitudeInput")
        self.magnitudeInput.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.magnitudeInput)


        self.retranslateUi(FrequencyInput)

        QMetaObject.connectSlotsByName(FrequencyInput)
    # setupUi

    def retranslateUi(self, FrequencyInput):
        FrequencyInput.setWindowTitle(QCoreApplication.translate("FrequencyInput", u"Form", None))

    # retranslateUi

