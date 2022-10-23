# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'solutiondialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout,
    QWidget)

from ..bandselect import BandSelect
from ..frequencyentry import FrequencyEntry
from ..solutioncanvas import SolutionCanvas
from ..weightsframe import WeightsFrame
from . import rc_icons

class Ui_SolutionDialog(object):
    def setupUi(self, SolutionDialog):
        if not SolutionDialog.objectName():
            SolutionDialog.setObjectName(u"SolutionDialog")
        SolutionDialog.resize(1099, 942)
        self.horizontalLayout = QHBoxLayout(SolutionDialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_2 = QWidget(SolutionDialog)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_4 = QVBoxLayout(self.widget_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox = QGroupBox(self.widget_2)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.chromosomeText = QPlainTextEdit(self.groupBox)
        self.chromosomeText.setObjectName(u"chromosomeText")
        self.chromosomeText.setMaximumSize(QSize(16777215, 70))

        self.verticalLayout_2.addWidget(self.chromosomeText, 0, Qt.AlignTop)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.groupBox_5 = QGroupBox(self.widget_2)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.weightsFrame = WeightsFrame(self.groupBox_5)
        self.weightsFrame.setObjectName(u"weightsFrame")
        self.weightsFrame.setMinimumSize(QSize(0, 170))
        self.weightsFrame.setFrameShape(QFrame.NoFrame)

        self.verticalLayout_7.addWidget(self.weightsFrame)


        self.verticalLayout_4.addWidget(self.groupBox_5)

        self.groupBox_4 = QGroupBox(self.widget_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.widget_4 = BandSelect(self.groupBox_4)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMinimumSize(QSize(0, 100))

        self.verticalLayout_5.addWidget(self.widget_4)


        self.verticalLayout_4.addWidget(self.groupBox_4)

        self.groupBox_3 = QGroupBox(self.widget_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.toolButton_2 = QToolButton(self.groupBox_3)
        self.toolButton_2.setObjectName(u"toolButton_2")
        self.toolButton_2.setText(u"PushButton")
        icon = QIcon()
        icon.addFile(u":/icons/icons/Pinion.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton_2.setIcon(icon)
#if QT_CONFIG(shortcut)
        self.toolButton_2.setShortcut(u"")
#endif // QT_CONFIG(shortcut)

        self.horizontalLayout_2.addWidget(self.toolButton_2)


        self.verticalLayout_4.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.widget_2)
        self.groupBox_2.setObjectName(u"groupBox_2")

        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.groupBox_6 = QGroupBox(self.widget_2)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.startFrequencyInput = FrequencyEntry(self.groupBox_6)
        self.startFrequencyInput.setObjectName(u"startFrequencyInput")
        self.startFrequencyInput.setMinimumSize(QSize(150, 40))
        self.startFrequencyInput.setStyleSheet(u"")

        self.verticalLayout_6.addWidget(self.startFrequencyInput)


        self.verticalLayout_4.addWidget(self.groupBox_6)

        self.pushButton = QPushButton(self.widget_2)
        self.pushButton.setObjectName(u"pushButton")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/Sync.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon1)

        self.verticalLayout_4.addWidget(self.pushButton)


        self.horizontalLayout.addWidget(self.widget_2)

        self.widget = QWidget(SolutionDialog)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame = QFrame(self.widget)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(800, 800))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.solutionCanvas = SolutionCanvas(self.frame)
        self.solutionCanvas.setObjectName(u"solutionCanvas")

        self.verticalLayout.addWidget(self.solutionCanvas)


        self.verticalLayout_3.addWidget(self.frame)


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(SolutionDialog)

        self.pushButton.setDefault(True)


        QMetaObject.connectSlotsByName(SolutionDialog)
    # setupUi

    def retranslateUi(self, SolutionDialog):
        SolutionDialog.setWindowTitle(QCoreApplication.translate("SolutionDialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("SolutionDialog", u"Chromosome", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("SolutionDialog", u"Weights", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("SolutionDialog", u"Bands", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("SolutionDialog", u"Range of Interest", None))
        self.label.setText(QCoreApplication.translate("SolutionDialog", u"TextLabel", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("SolutionDialog", u"Settings", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("SolutionDialog", u"Test Frequency", None))
        self.pushButton.setText(QCoreApplication.translate("SolutionDialog", u" Recompute", None))
    # retranslateUi

