# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QHBoxLayout,
    QLabel, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTabWidget,
    QToolBar, QVBoxLayout, QWidget)

from ..bandselect import BandSelect
from ..bode_plot_canvas import BodePlotCanvas
from ..paginator import Paginator
from ..weightsframe import WeightsFrame
from . import rc_icons

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1182, 457)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(350, 0))
        self.tabWidget.setMaximumSize(QSize(350, 16777215))
        self.controlTab = QWidget()
        self.controlTab.setObjectName(u"controlTab")
        self.verticalLayout_6 = QVBoxLayout(self.controlTab)
        self.verticalLayout_6.setSpacing(10)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.widget_3 = QWidget(self.controlTab)
        self.widget_3.setObjectName(u"widget_3")
        self.formLayout = QFormLayout(self.widget_3)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout.setHorizontalSpacing(16)
        self.formLayout.setContentsMargins(40, 15, -1, 10)
        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"Monospace"])
        font.setPointSize(14)
        font.setBold(True)
        self.label.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(self.widget_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.label_3 = QLabel(self.widget_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.circuitLabel = QLabel(self.widget_3)
        self.circuitLabel.setObjectName(u"circuitLabel")
        font1 = QFont()
        font1.setFamilies([u"Monospace"])
        font1.setPointSize(12)
        self.circuitLabel.setFont(font1)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.circuitLabel)

        self.generationLabel = QLabel(self.widget_3)
        self.generationLabel.setObjectName(u"generationLabel")
        self.generationLabel.setFont(font1)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.generationLabel)

        self.computeTimeLabel = QLabel(self.widget_3)
        self.computeTimeLabel.setObjectName(u"computeTimeLabel")
        self.computeTimeLabel.setFont(font1)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.computeTimeLabel)

        self.label_7 = QLabel(self.widget_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_7)

        self.fitnessLabel_2 = QLabel(self.widget_3)
        self.fitnessLabel_2.setObjectName(u"fitnessLabel_2")
        self.fitnessLabel_2.setFont(font1)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.fitnessLabel_2)


        self.verticalLayout_6.addWidget(self.widget_3)

        self.frame_2 = QFrame(self.controlTab)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.miniplot = BodePlotCanvas(self.frame_2)
        self.miniplot.setObjectName(u"miniplot")
        self.miniplot.setMinimumSize(QSize(300, 150))
        self.miniplot.setMaximumSize(QSize(300, 150))
        self.miniplot.setLayoutDirection(Qt.LeftToRight)
        self.miniplot.setStyleSheet(u"background-color:white")

        self.verticalLayout_4.addWidget(self.miniplot)


        self.verticalLayout_6.addWidget(self.frame_2, 0, Qt.AlignHCenter)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.startStopButton = QPushButton(self.controlTab)
        self.startStopButton.setObjectName(u"startStopButton")
        font2 = QFont()
        font2.setBold(True)
        self.startStopButton.setFont(font2)
        icon = QIcon()
        icon.addFile(u":/icons/icons/Yes.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.startStopButton.setIcon(icon)

        self.horizontalLayout_4.addWidget(self.startStopButton)

        self.stopResetButton = QPushButton(self.controlTab)
        self.stopResetButton.setObjectName(u"stopResetButton")
        self.stopResetButton.setEnabled(False)
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/Abort.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.stopResetButton.setIcon(icon1)

        self.horizontalLayout_4.addWidget(self.stopResetButton)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.tabWidget.addTab(self.controlTab, "")
        self.bandsTab = QWidget()
        self.bandsTab.setObjectName(u"bandsTab")
        self.bandsTab.setEnabled(True)
        self.widget_4 = BandSelect(self.bandsTab)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setGeometry(QRect(40, 90, 251, 171))
        self.tabWidget.addTab(self.bandsTab, "")
        self.weightControlsTab = QWidget()
        self.weightControlsTab.setObjectName(u"weightControlsTab")
        self.verticalLayout_7 = QVBoxLayout(self.weightControlsTab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.weightsFrame = WeightsFrame(self.weightControlsTab)
        self.weightsFrame.setObjectName(u"weightsFrame")
        self.weightsFrame.setFrameShape(QFrame.StyledPanel)
        self.weightsFrame.setFrameShadow(QFrame.Raised)

        self.verticalLayout_7.addWidget(self.weightsFrame)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.weightControlsTab, "")
        self.settingsTab = QWidget()
        self.settingsTab.setObjectName(u"settingsTab")
        self.tabWidget.addTab(self.settingsTab, "")

        self.horizontalLayout.addWidget(self.tabWidget, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 9, 0, 0)
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(0, 35))
        self.widget_2.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.paginator = Paginator(self.widget_2)
        self.paginator.setObjectName(u"paginator")
        self.paginator.setMinimumSize(QSize(300, 0))
        self.paginator.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_2.addWidget(self.paginator)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.horizontalLayoutControl = QWidget(self.widget_2)
        self.horizontalLayoutControl.setObjectName(u"horizontalLayoutControl")
        self.horizontalLayoutControl.setMinimumSize(QSize(100, 0))
        self.verticalLayout_5 = QVBoxLayout(self.horizontalLayoutControl)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_2.addWidget(self.horizontalLayoutControl)


        self.verticalLayout_3.addWidget(self.widget_2)

        self.frame = QFrame(self.widget)
        self.frame.setObjectName(u"frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.mainBodePlot = BodePlotCanvas(self.frame)
        self.mainBodePlot.setObjectName(u"mainBodePlot")
        self.mainBodePlot.setMinimumSize(QSize(800, 300))
        self.mainBodePlot.setMaximumSize(QSize(800, 300))
        self.mainBodePlot.setLayoutDirection(Qt.LeftToRight)
        self.mainBodePlot.setStyleSheet(u"background-color:white")

        self.verticalLayout_2.addWidget(self.mainBodePlot)


        self.verticalLayout_3.addWidget(self.frame)

        self.frame_3 = QFrame(self.widget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.fitnessLabel = QLabel(self.frame_3)
        self.fitnessLabel.setObjectName(u"fitnessLabel")
        font3 = QFont()
        font3.setFamilies([u"Monospace"])
        font3.setPointSize(14)
        self.fitnessLabel.setFont(font3)
        self.fitnessLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.fitnessLabel)

        self.displaySolutionDialogBtn = QPushButton(self.frame_3)
        self.displaySolutionDialogBtn.setObjectName(u"displaySolutionDialogBtn")
        self.displaySolutionDialogBtn.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.displaySolutionDialogBtn)


        self.verticalLayout_3.addWidget(self.frame_3)


        self.horizontalLayout.addWidget(self.widget, 0, Qt.AlignTop)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1182, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Project: Electrify", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Circuit", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Generation", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Sim Time", None))
        self.circuitLabel.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.generationLabel.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.computeTimeLabel.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Fitness", None))
        self.fitnessLabel_2.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.startStopButton.setText(QCoreApplication.translate("MainWindow", u"Begin", None))
        self.stopResetButton.setText(QCoreApplication.translate("MainWindow", u"Halt", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.controlTab), QCoreApplication.translate("MainWindow", u"Control", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bandsTab), QCoreApplication.translate("MainWindow", u"Bands", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.weightControlsTab), QCoreApplication.translate("MainWindow", u"Weights", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settingsTab), QCoreApplication.translate("MainWindow", u"Settings", None))
        self.fitnessLabel.setText("")
        self.displaySolutionDialogBtn.setText(QCoreApplication.translate("MainWindow", u"View Solution", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

