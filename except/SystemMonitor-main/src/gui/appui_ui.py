# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'appui.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(923, 431)
        MainWindow.setStyleSheet(u"#RamProgressBar {\n"
"    text-align: center;\n"
"}\n"
"#RamProgressBar::chunk {\n"
"    background-color: #3498db;\n"
"}\n"
"#CpuProgressBar {\n"
"    text-align: center;\n"
"}\n"
"#CpuProgressBar::chunk {\n"
"    background-color: #2ecc71;\n"
"}\n"
"#DiskProgressBar {\n"
"    text-align: center;\n"
"}\n"
"#DiskProgressBar::chunk {\n"
"   background-color: #9b59b6;\n"
"}\n"
"QProgressBar\n"
"{\n"
"border: solid grey;\n"
"border-radius: 15px;\n"
"color: black;\n"
"}\n"
"QProgressBar::chunk \n"
"{\n"
"border-radius :15px;\n"
"}    \n"
"")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QSize(10, 20))
        self.label_5.setMaximumSize(QSize(65, 15))

        self.verticalLayout.addWidget(self.label_5, 0, Qt.AlignHCenter)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(60, 50))
        self.label.setMaximumSize(QSize(60, 50))

        self.verticalLayout.addWidget(self.label)

        self.RamProgressBar = QProgressBar(self.centralwidget)
        self.RamProgressBar.setObjectName(u"RamProgressBar")
        sizePolicy.setHeightForWidth(self.RamProgressBar.sizePolicy().hasHeightForWidth())
        self.RamProgressBar.setSizePolicy(sizePolicy)
        self.RamProgressBar.setMinimumSize(QSize(461, 31))
        self.RamProgressBar.setMaximumSize(QSize(461, 31))
        self.RamProgressBar.setValue(0)
        self.RamProgressBar.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.RamProgressBar)

        self.ram_info = QLabel(self.centralwidget)
        self.ram_info.setObjectName(u"ram_info")

        self.verticalLayout.addWidget(self.ram_info)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(60, 50))
        self.label_2.setMaximumSize(QSize(60, 50))

        self.verticalLayout.addWidget(self.label_2)

        self.CpuProgressBar = QProgressBar(self.centralwidget)
        self.CpuProgressBar.setObjectName(u"CpuProgressBar")
        sizePolicy.setHeightForWidth(self.CpuProgressBar.sizePolicy().hasHeightForWidth())
        self.CpuProgressBar.setSizePolicy(sizePolicy)
        self.CpuProgressBar.setMinimumSize(QSize(461, 31))
        self.CpuProgressBar.setMaximumSize(QSize(461, 31))
        self.CpuProgressBar.setValue(0)

        self.verticalLayout.addWidget(self.CpuProgressBar)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QSize(60, 50))
        self.label_3.setMaximumSize(QSize(60, 50))

        self.verticalLayout.addWidget(self.label_3)

        self.DiskProgressBar = QProgressBar(self.centralwidget)
        self.DiskProgressBar.setObjectName(u"DiskProgressBar")
        sizePolicy.setHeightForWidth(self.DiskProgressBar.sizePolicy().hasHeightForWidth())
        self.DiskProgressBar.setSizePolicy(sizePolicy)
        self.DiskProgressBar.setMinimumSize(QSize(461, 31))
        self.DiskProgressBar.setMaximumSize(QSize(461, 31))
        self.DiskProgressBar.setValue(0)
        self.DiskProgressBar.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.DiskProgressBar)

        self.diskinfo = QLabel(self.centralwidget)
        self.diskinfo.setObjectName(u"diskinfo")

        self.verticalLayout.addWidget(self.diskinfo)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4, 0, Qt.AlignHCenter)

        self.host = QLabel(self.centralwidget)
        self.host.setObjectName(u"host")
        sizePolicy.setHeightForWidth(self.host.sizePolicy().hasHeightForWidth())
        self.host.setSizePolicy(sizePolicy)
        self.host.setMinimumSize(QSize(301, 40))

        self.verticalLayout_2.addWidget(self.host)

        self.pltf = QLabel(self.centralwidget)
        self.pltf.setObjectName(u"pltf")
        sizePolicy.setHeightForWidth(self.pltf.sizePolicy().hasHeightForWidth())
        self.pltf.setSizePolicy(sizePolicy)
        self.pltf.setMinimumSize(QSize(301, 31))

        self.verticalLayout_2.addWidget(self.pltf)

        self.pltf_ver = QLabel(self.centralwidget)
        self.pltf_ver.setObjectName(u"pltf_ver")
        sizePolicy.setHeightForWidth(self.pltf_ver.sizePolicy().hasHeightForWidth())
        self.pltf_ver.setSizePolicy(sizePolicy)
        self.pltf_ver.setMinimumSize(QSize(301, 31))

        self.verticalLayout_2.addWidget(self.pltf_ver)

        self.pltf_re = QLabel(self.centralwidget)
        self.pltf_re.setObjectName(u"pltf_re")
        sizePolicy.setHeightForWidth(self.pltf_re.sizePolicy().hasHeightForWidth())
        self.pltf_re.setSizePolicy(sizePolicy)
        self.pltf_re.setMinimumSize(QSize(301, 31))

        self.verticalLayout_2.addWidget(self.pltf_re)

        self.ram = QLabel(self.centralwidget)
        self.ram.setObjectName(u"ram")
        sizePolicy.setHeightForWidth(self.ram.sizePolicy().hasHeightForWidth())
        self.ram.setSizePolicy(sizePolicy)
        self.ram.setMinimumSize(QSize(301, 31))

        self.verticalLayout_2.addWidget(self.ram)

        self.cpu = QLabel(self.centralwidget)
        self.cpu.setObjectName(u"cpu")
        sizePolicy.setHeightForWidth(self.cpu.sizePolicy().hasHeightForWidth())
        self.cpu.setSizePolicy(sizePolicy)
        self.cpu.setMinimumSize(QSize(301, 31))

        self.verticalLayout_2.addWidget(self.cpu)

        self.cpu_cores = QLabel(self.centralwidget)
        self.cpu_cores.setObjectName(u"cpu_cores")
        sizePolicy.setHeightForWidth(self.cpu_cores.sizePolicy().hasHeightForWidth())
        self.cpu_cores.setSizePolicy(sizePolicy)
        self.cpu_cores.setMinimumSize(QSize(301, 31))

        self.verticalLayout_2.addWidget(self.cpu_cores)

        self.ip = QLabel(self.centralwidget)
        self.ip.setObjectName(u"ip")
        sizePolicy.setHeightForWidth(self.ip.sizePolicy().hasHeightForWidth())
        self.ip.setSizePolicy(sizePolicy)
        self.ip.setMinimumSize(QSize(301, 31))

        self.verticalLayout_2.addWidget(self.ip)

        self.mac = QLabel(self.centralwidget)
        self.mac.setObjectName(u"mac")
        sizePolicy.setHeightForWidth(self.mac.sizePolicy().hasHeightForWidth())
        self.mac.setSizePolicy(sizePolicy)
        self.mac.setMinimumSize(QSize(301, 31))

        self.verticalLayout_2.addWidget(self.mac)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 923, 21))
        self.menuMenu = QMenu(self.menubar)
        self.menuMenu.setObjectName(u"menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.menubar.addAction(self.menuMenu.menuAction())
        self.menuMenu.addAction(self.actionAbout)
        self.menuMenu.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SystemMonitor 1.0", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Resources", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Memory:", None))
        self.ram_info.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Cpu:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Disk:", None))
        self.diskinfo.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"System Informations", None))
        self.host.setText(QCoreApplication.translate("MainWindow", u"Hostname:", None))
        self.pltf.setText(QCoreApplication.translate("MainWindow", u"Platform:", None))
        self.pltf_ver.setText(QCoreApplication.translate("MainWindow", u"Platform-version:", None))
        self.pltf_re.setText(QCoreApplication.translate("MainWindow", u"Platform-release:", None))
        self.ram.setText(QCoreApplication.translate("MainWindow", u"RAM:", None))
        self.cpu.setText(QCoreApplication.translate("MainWindow", u"Processor:", None))
        self.cpu_cores.setText(QCoreApplication.translate("MainWindow", u"CPU-Cores:", None))
        self.ip.setText(QCoreApplication.translate("MainWindow", u"Ip-address:", None))
        self.mac.setText(QCoreApplication.translate("MainWindow", u"Mac-address:", None))
        self.menuMenu.setTitle(QCoreApplication.translate("MainWindow", u"Menu", None))
    # retranslateUi

