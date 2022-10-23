# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'namedslider.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QSizePolicy, QSlider, QWidget)

class Ui_NamedSlider(object):
    def setupUi(self, NamedSlider):
        if not NamedSlider.objectName():
            NamedSlider.setObjectName(u"NamedSlider")
        NamedSlider.resize(250, 31)
        NamedSlider.setMinimumSize(QSize(250, 0))
        self.horizontalLayout = QHBoxLayout(NamedSlider)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 3, -1, 3)
        self.sliderNameLabel = QLabel(NamedSlider)
        self.sliderNameLabel.setObjectName(u"sliderNameLabel")
        self.sliderNameLabel.setMinimumSize(QSize(70, 0))
        self.sliderNameLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.sliderNameLabel)

        self.line = QFrame(NamedSlider)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setFrameShape(QFrame.VLine)

        self.horizontalLayout.addWidget(self.line)

        self.valueSlider = QSlider(NamedSlider)
        self.valueSlider.setObjectName(u"valueSlider")
        self.valueSlider.setMaximum(100)
        self.valueSlider.setOrientation(Qt.Horizontal)
        self.valueSlider.setTickPosition(QSlider.TicksBothSides)

        self.horizontalLayout.addWidget(self.valueSlider)

        self.line_2 = QFrame(NamedSlider)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShadow(QFrame.Plain)
        self.line_2.setFrameShape(QFrame.VLine)

        self.horizontalLayout.addWidget(self.line_2)

        self.sliderValueLabel = QLabel(NamedSlider)
        self.sliderValueLabel.setObjectName(u"sliderValueLabel")
        self.sliderValueLabel.setMinimumSize(QSize(30, 0))
        self.sliderValueLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.sliderValueLabel)


        self.retranslateUi(NamedSlider)

        QMetaObject.connectSlotsByName(NamedSlider)
    # setupUi

    def retranslateUi(self, NamedSlider):
        NamedSlider.setWindowTitle(QCoreApplication.translate("NamedSlider", u"Form", None))
        self.sliderNameLabel.setText(QCoreApplication.translate("NamedSlider", u"Title", None))
        self.sliderValueLabel.setText(QCoreApplication.translate("NamedSlider", u"0", None))
    # retranslateUi

