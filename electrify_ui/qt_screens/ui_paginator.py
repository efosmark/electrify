# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'paginator.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)

class Ui_Paginator(object):
    def setupUi(self, Paginator):
        if not Paginator.objectName():
            Paginator.setObjectName(u"Paginator")
        Paginator.resize(200, 25)
        Paginator.setMinimumSize(QSize(200, 0))
        Paginator.setMaximumSize(QSize(200, 16777215))
        self.horizontalLayout = QHBoxLayout(Paginator)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.prevButton = QPushButton(Paginator)
        self.prevButton.setObjectName(u"prevButton")
        self.prevButton.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.prevButton)

        self.nextButton = QPushButton(Paginator)
        self.nextButton.setObjectName(u"nextButton")
        self.nextButton.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.nextButton)

        self.pageLabel = QLabel(Paginator)
        self.pageLabel.setObjectName(u"pageLabel")
        self.pageLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.pageLabel)


        self.retranslateUi(Paginator)

        QMetaObject.connectSlotsByName(Paginator)
    # setupUi

    def retranslateUi(self, Paginator):
        self.prevButton.setText(QCoreApplication.translate("Paginator", u"<", None))
        self.nextButton.setText(QCoreApplication.translate("Paginator", u">", None))
        self.pageLabel.setText(QCoreApplication.translate("Paginator", u"1/1", None))
        pass
    # retranslateUi

