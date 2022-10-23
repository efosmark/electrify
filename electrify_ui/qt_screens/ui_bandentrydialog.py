# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bandentrydialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGroupBox, QHBoxLayout, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from ..frequencyentry import FrequencyEntry

class Ui_BandEntryDialog(object):
    def setupUi(self, BandEntryDialog):
        if not BandEntryDialog.objectName():
            BandEntryDialog.setObjectName(u"BandEntryDialog")
        BandEntryDialog.setWindowModality(Qt.ApplicationModal)
        BandEntryDialog.resize(370, 130)
        BandEntryDialog.setMinimumSize(QSize(370, 130))
        BandEntryDialog.setMaximumSize(QSize(370, 130))
        BandEntryDialog.setWindowTitle(u"Enter Band Frequencies")
        BandEntryDialog.setSizeGripEnabled(False)
        BandEntryDialog.setModal(True)
        self.verticalLayout_3 = QVBoxLayout(BandEntryDialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget_3 = QWidget(BandEntryDialog)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMaximumSize(QSize(350, 16777215))
        self.horizontalLayout = QHBoxLayout(self.widget_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(self.widget_3)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setTitle(u"Start Frequency")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.startFrequencyInput = FrequencyEntry(self.groupBox)
        self.startFrequencyInput.setObjectName(u"startFrequencyInput")
        self.startFrequencyInput.setMinimumSize(QSize(150, 30))
        self.startFrequencyInput.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.startFrequencyInput)


        self.horizontalLayout.addWidget(self.groupBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.groupBox_2 = QGroupBox(self.widget_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setTitle(u"End Frequency")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.endFrequencyInput = FrequencyEntry(self.groupBox_2)
        self.endFrequencyInput.setObjectName(u"endFrequencyInput")
        self.endFrequencyInput.setMinimumSize(QSize(150, 30))
        self.endFrequencyInput.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.endFrequencyInput)


        self.horizontalLayout.addWidget(self.groupBox_2)


        self.verticalLayout_3.addWidget(self.widget_3)

        self.validationLabel = QLabel(BandEntryDialog)
        self.validationLabel.setObjectName(u"validationLabel")
        font = QFont()
        font.setFamilies([u"Monospace"])
        font.setPointSize(12)
        self.validationLabel.setFont(font)
        self.validationLabel.setStyleSheet(u"color:red")
        self.validationLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.validationLabel)

        self.dialogButtonBox = QDialogButtonBox(BandEntryDialog)
        self.dialogButtonBox.setObjectName(u"dialogButtonBox")
        self.dialogButtonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_3.addWidget(self.dialogButtonBox)


        self.retranslateUi(BandEntryDialog)

        QMetaObject.connectSlotsByName(BandEntryDialog)
    # setupUi

    def retranslateUi(self, BandEntryDialog):
        self.validationLabel.setText("")
        pass
    # retranslateUi

