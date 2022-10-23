# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bandinputdialog.ui'
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

from ..frequencyinput import FrequencyInput

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.ApplicationModal)
        Dialog.resize(400, 160)
        Dialog.setMinimumSize(QSize(400, 160))
        Dialog.setMaximumSize(QSize(400, 160))
        Dialog.setWindowTitle(u"Enter Band Frequencies")
        Dialog.setModal(True)
        self.verticalLayout_3 = QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget_3 = QWidget(Dialog)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout = QHBoxLayout(self.widget_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(self.widget_3)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Monospace"])
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.startFrequencyInput = FrequencyInput(self.groupBox)
        self.startFrequencyInput.setObjectName(u"startFrequencyInput")
        self.startFrequencyInput.setMinimumSize(QSize(150, 32))
        self.startFrequencyInput.setMaximumSize(QSize(150, 32))
        self.startFrequencyInput.setStyleSheet(u"border:1px solid black")

        self.verticalLayout.addWidget(self.startFrequencyInput, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.horizontalLayout.addWidget(self.groupBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.groupBox_2 = QGroupBox(self.widget_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setFont(font)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.endFrequencyInput = FrequencyInput(self.groupBox_2)
        self.endFrequencyInput.setObjectName(u"endFrequencyInput")
        self.endFrequencyInput.setMinimumSize(QSize(150, 32))
        self.endFrequencyInput.setMaximumSize(QSize(150, 32))
        self.endFrequencyInput.setStyleSheet(u"border:1px solid black")

        self.verticalLayout_2.addWidget(self.endFrequencyInput, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.horizontalLayout.addWidget(self.groupBox_2)


        self.verticalLayout_3.addWidget(self.widget_3, 0, Qt.AlignTop)

        self.validationLabel = QLabel(Dialog)
        self.validationLabel.setObjectName(u"validationLabel")
        font1 = QFont()
        font1.setFamilies([u"Monospace"])
        font1.setPointSize(12)
        self.validationLabel.setFont(font1)
        self.validationLabel.setStyleSheet(u"color:red")
        self.validationLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.validationLabel)

        self.dialogButtonBox = QDialogButtonBox(Dialog)
        self.dialogButtonBox.setObjectName(u"dialogButtonBox")
        self.dialogButtonBox.setOrientation(Qt.Horizontal)
        self.dialogButtonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_3.addWidget(self.dialogButtonBox)


        self.retranslateUi(Dialog)
        self.dialogButtonBox.accepted.connect(Dialog.accept)
        self.dialogButtonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Start Frequency", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"End Frequency", None))
        self.validationLabel.setText("")
        pass
    # retranslateUi

