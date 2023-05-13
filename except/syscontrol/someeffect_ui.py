# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'someeffect.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1044, 771)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.shapka = QWidget(self.centralwidget)
        self.shapka.setObjectName(u"shapka")
        self.shapka.setGeometry(QRect(0, 0, 1041, 41))
        font = QFont()
        font.setFamilies([u"Arial Black"])
        font.setBold(True)
        self.shapka.setFont(font)
        self.shapka.setMouseTracking(False)
        self.shapka.setStyleSheet(u"")
        self.main_button1 = QPushButton(self.shapka)
        self.main_button1.setObjectName(u"main_button1")
        self.main_button1.setGeometry(QRect(160, 0, 81, 41))
        self.main_button2 = QPushButton(self.shapka)
        self.main_button2.setObjectName(u"main_button2")
        self.main_button2.setGeometry(QRect(250, 0, 81, 41))
        self.main_button3 = QPushButton(self.shapka)
        self.main_button3.setObjectName(u"main_button3")
        self.main_button3.setGeometry(QRect(340, 0, 81, 41))
        self.main_button4 = QPushButton(self.shapka)
        self.main_button4.setObjectName(u"main_button4")
        self.main_button4.setGeometry(QRect(430, 0, 81, 41))
        self.pushButton_9 = QPushButton(self.shapka)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setGeometry(QRect(520, 0, 81, 41))
        self.logo = QWidget(self.shapka)
        self.logo.setObjectName(u"logo")
        self.logo.setGeometry(QRect(-1, -1, 151, 41))
        self.podshapka = QWidget(self.centralwidget)
        self.podshapka.setObjectName(u"podshapka")
        self.podshapka.setGeometry(QRect(0, 40, 1041, 31))
        font1 = QFont()
        font1.setFamilies([u"Arial Narrow"])
        font1.setPointSize(10)
        self.podshapka.setFont(font1)
        self.pushButton_10 = QPushButton(self.podshapka)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setGeometry(QRect(10, 0, 71, 31))
        self.pushButton_11 = QPushButton(self.podshapka)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setGeometry(QRect(90, 0, 71, 31))
        self.pushButton_12 = QPushButton(self.podshapka)
        self.pushButton_12.setObjectName(u"pushButton_12")
        self.pushButton_12.setGeometry(QRect(170, 0, 71, 31))
        self.pushButton_13 = QPushButton(self.podshapka)
        self.pushButton_13.setObjectName(u"pushButton_13")
        self.pushButton_13.setGeometry(QRect(250, 0, 71, 31))
        self.pushButton_14 = QPushButton(self.podshapka)
        self.pushButton_14.setObjectName(u"pushButton_14")
        self.pushButton_14.setGeometry(QRect(330, 0, 71, 31))
        self.pushButton_15 = QPushButton(self.podshapka)
        self.pushButton_15.setObjectName(u"pushButton_15")
        self.pushButton_15.setGeometry(QRect(410, 0, 71, 31))
        self.pushButton_16 = QPushButton(self.podshapka)
        self.pushButton_16.setObjectName(u"pushButton_16")
        self.pushButton_16.setGeometry(QRect(490, 0, 71, 31))
        self.pushButton_17 = QPushButton(self.podshapka)
        self.pushButton_17.setObjectName(u"pushButton_17")
        self.pushButton_17.setGeometry(QRect(570, 0, 71, 31))
        self.mainopen = QGroupBox(self.centralwidget)
        self.mainopen.setObjectName(u"mainopen")
        self.mainopen.setGeometry(QRect(0, 80, 1041, 651))
        self.horizontalLayoutWidget = QWidget(self.mainopen)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 40, 1021, 41))
        self.main_buttons = QHBoxLayout(self.horizontalLayoutWidget)
        self.main_buttons.setObjectName(u"main_buttons")
        self.main_buttons.setContentsMargins(0, 0, 0, 0)
        self.pushButton_2 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.main_buttons.addWidget(self.pushButton_2)

        self.label_6 = QLabel(self.horizontalLayoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.main_buttons.addWidget(self.label_6)

        self.pushButton = QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.main_buttons.addWidget(self.pushButton)

        self.label_7 = QLabel(self.horizontalLayoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.main_buttons.addWidget(self.label_7)

        self.pushButton_3 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.main_buttons.addWidget(self.pushButton_3)

        self.label_8 = QLabel(self.horizontalLayoutWidget)
        self.label_8.setObjectName(u"label_8")

        self.main_buttons.addWidget(self.label_8)

        self.pushButton_4 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.main_buttons.addWidget(self.pushButton_4)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.main_buttons.addItem(self.horizontalSpacer)

        self.changes_active = QFrame(self.mainopen)
        self.changes_active.setObjectName(u"changes_active")
        self.changes_active.setGeometry(QRect(0, 90, 1031, 551))
        self.changes_active.setFrameShape(QFrame.StyledPanel)
        self.changes_active.setFrameShadow(QFrame.Raised)
        self.widget = QWidget(self.changes_active)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 10, 291, 201))
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(10, 20, 281, 181))
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 0, 231, 21))
        self.widget_3 = QWidget(self.changes_active)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setGeometry(QRect(310, 0, 471, 211))
        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setGeometry(QRect(10, 20, 461, 191))
        self.label_2 = QLabel(self.widget_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 0, 291, 21))
        self.widget_5 = QWidget(self.changes_active)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setGeometry(QRect(0, 220, 291, 261))
        self.widget_6 = QWidget(self.widget_5)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setGeometry(QRect(10, 20, 281, 241))
        self.label_3 = QLabel(self.widget_5)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 0, 281, 21))
        self.widget_7 = QWidget(self.changes_active)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setGeometry(QRect(310, 220, 471, 261))
        self.widget_9 = QWidget(self.widget_7)
        self.widget_9.setObjectName(u"widget_9")
        self.widget_9.setGeometry(QRect(10, 20, 461, 241))
        self.label_5 = QLabel(self.widget_7)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 0, 291, 21))
        self.line = QFrame(self.mainopen)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(0, 30, 1059, 3))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1044, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.main_button1.setText(QCoreApplication.translate("MainWindow", u"\u0410\u043a\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u044c", None))
        self.main_button2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.main_button3.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.main_button4.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_13.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_14.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_15.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_16.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_17.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.mainopen.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"/", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"/", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"/", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

