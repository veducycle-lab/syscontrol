from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QMenu, QAction, QWidget,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings, Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

from blocks_admin.PERSONS_STATISTIC import PersonStatistic
from blocks_admin.CHANGE_REDACTE_DB import SQLViewer
from blocks_admin.GRAPH import GraphWidget, InfoLabel
from blocks_admin.PROCESS_EXPLORER import ProcessManager
from blocks_admin.SYSTEM_INFO import SystemInfoWidget
from blocks_admin.PERSONAL_STATISTICS import ScrollAreaWidget
from blocks_admin.PDF_VIEWER1 import PDFWidget1
from blocks_admin.PDF_VIEWER2 import PDFWidget2
from blocks_admin.PERSON_ACTIVITY_PC import PersonActivity
from blocks_admin.PC_LOGS import PClogs
from blocks_admin.CHECKED_DB import DBController


import subprocess


class AdminTools(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('ADMINTOOLS.ui', self)
        self.setWindowTitle("SAM")
        self.setWindowIcon(QIcon("icon.png"))
        # Назначение обработчиков для main_button
        self.main_button0.clicked.connect(self.show_mainopen0)
        self.main_button1.clicked.connect(self.show_under_1)
        self.main_button2.clicked.connect(self.show_under_2)
        self.main_button3.clicked.connect(self.show_under_3)
        self.main_button4.clicked.connect(self.show_under_4)
        self.main_button5.clicked.connect(self.show_under_5)
        
        # Назначение обработчиков для pushButton_1_X
        self.pushButton_1_1.clicked.connect(self.show_changes_active1_1)
        self.pushButton_1_2.clicked.connect(self.show_changes_active1_2)
        self.pushButton_1_3.clicked.connect(self.show_changes_active1_3)
        
        # Назначение обработчиков для pushButton_2_X
        self.pushButton_2_1.clicked.connect(self.show_changes_active2_1)
        self.pushButton_2_2.clicked.connect(self.show_changes_active2_2)
        
        # Назначение обработчиков для pushButton_3_X
        self.pushButton_3_1.clicked.connect(self.show_changes_active3_1)
        self.pushButton_3_2.clicked.connect(self.show_changes_active3_2)
        
        # Назначение обработчиков для pushButton_4_X
        self.pushButton_4_1.clicked.connect(self.show_changes_active4_1)
        self.pushButton_4_2.clicked.connect(self.show_changes_active4_2)
        
        # Назначение обработчиков для pushButton_5_X
        self.pushButton_5_2.clicked.connect(self.show_changes_active5_2)
        self.pushButton_5_4.clicked.connect(self.show_changes_active5_4)

        self.mainopen0_label = QLabel(self.mainopen0)
        self.mainopen0_label.setPixmap(QPixmap("screen_main.png"))
        
        
        # Скрытие всех виджетов changes_active
        self.hide_changes_active()
        
        # Открытие mainopen0 при запуске приложения
        self.show_mainopen0()
        self.save_session()
    
    def bring_to_front(self, window):
        window.setWindowState(window.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        window.activateWindow()


    def enable_mouse_events_recursive(self, widget):
        # Рекурсивно устанавливаем флаг Qt.WA_TransparentForMouseEvents для каждого виджета
        widget.setAttribute(Qt.WA_TransparentForMouseEvents)
        for child_widget in widget.findChildren(QWidget):
            self.enable_mouse_events_recursive(child_widget)

    def hide_changes_active(self):
        # Скрытие всех виджетов changes_active
        self.changes_active1_1.hide()
        self.changes_active1_2.hide()
        self.changes_active1_3.hide()
        self.changes_active2_1.hide()
        self.changes_active2_2.hide()
        self.changes_active3_1.hide()
        self.changes_active3_2.hide()
        self.changes_active4_1.hide()
        self.changes_active4_2.hide()
        self.changes_active5_2.hide()
        self.changes_active5_4.hide()
        
    def show_mainopen0(self):
        self.hide_changes_active()
        self.mainopen0.show()
        self.mainopen0.raise_()
        self.under_1.hide()
        self.under_2.hide()
        self.under_3.hide()
        self.under_4.hide()
        self.under_5.hide()

        
        # Добавление картинки в mainopen0
        pixmap = QPixmap('screen_main.png')  # Укажите путь к вашему изображению
        
        scaled_pixmap = pixmap.scaled(1901, 890)
        label = QLabel(self.mainopen0)
        label.setPixmap(scaled_pixmap)
        label.setAlignment(Qt.AlignCenter)
        label.setGeometry(0, 0, self.mainopen0.width(), self.mainopen0.height())
        label.show()
        
    def show_under_1(self):
        self.hide_changes_active()
        self.mainopen0.hide()
        self.under_1.show()
        self.under_1.raise_()
        self.under_2.hide()
        self.under_3.hide()
        self.under_4.hide()
        self.under_5.hide()
        self.bring_to_front(self.under_1)
        
    def show_under_2(self):
        self.hide_changes_active()
        self.mainopen0.hide()
        self.under_1.hide()
        self.under_2.show()
        self.under_2.raise_()
        self.under_3.hide()
        self.under_4.hide()
        self.under_5.hide()
        self.bring_to_front(self.under_2)
        
    def show_under_3(self):
        self.hide_changes_active()
        self.mainopen0.hide()
        self.under_1.hide()
        self.under_2.hide()
        self.under_3.show()
        self.under_3.raise_()
        self.under_4.hide()
        self.under_5.hide()
        self.bring_to_front(self.under_3)
        
    def show_under_4(self):
        self.hide_changes_active()
        self.mainopen0.hide()
        self.under_1.hide()
        self.under_2.hide()
        self.under_3.hide()
        self.under_4.show()
        self.under_4.raise_()
        self.under_5.hide()
        self.bring_to_front(self.under_4)
        
    def show_under_5(self):
        self.hide_changes_active()
        self.mainopen0.hide()
        self.under_1.hide()
        self.under_2.hide()
        self.under_3.hide()
        self.under_4.hide()
        self.under_5.show()
        self.under_5.raise_()
        self.bring_to_front(self.under_5)
        
    def show_changes_active1_1(self):
        self.hide_changes_active()
        sys_info = PersonStatistic()
        sys_info.setParent(self.changes_active1_1)
        sys_info.show()
        self.enable_mouse_events_recursive(sys_info)
        sys_info.setFocus()
        self.bring_to_front(self.changes_active1_1)
        self.changes_active1_1.show()
        
    def show_changes_active1_2(self):
        self.hide_changes_active()
        pers_active = PersonActivity()
        pers_active.setParent(self.changes_active1_2)
        pers_active.show()
        self.changes_active1_2.show()
        self.bring_to_front(self.changes_active1_2)
        self.changes_active1_2.raise_()
        
    def show_changes_active1_3(self):
        self.hide_changes_active()
        sys_info = ScrollAreaWidget()
        sys_info.setParent(self.changes_active1_3)
        sys_info.show()
        self.changes_active1_3.show()
        self.bring_to_front(self.changes_active1_3)
        self.changes_active1_3.raise_()
        
    def show_changes_active2_1(self):
        self.hide_changes_active()
        pc_logs = PClogs()
        pc_logs.setParent(self.changes_active2_1)
        pc_logs.show()
        self.changes_active2_1.show()
        self.bring_to_front(self.changes_active2_1)
        self.changes_active2_1.raise_()
        
    def show_changes_active2_2(self):
        self.hide_changes_active()
        self.changes_active2_2.show()
        graph_widget = GraphWidget()
        graph_widget.info_label = InfoLabel()
        graph_widget.plot_graph()
        graph_widget.canvas.mpl_connect('button_press_event', graph_widget.node_clicked)
        graph_widget.setParent(self.graph)
        self.enable_mouse_events_recursive(graph_widget)
        self.bring_to_front(self.changes_active2_2)
        graph_widget.show()
        info_label = graph_widget.info_label
        print(info_label)
        info_label.setParent(self.about_network)
        info_label.show()

    def show_changes_active3_1(self):
        self.hide_changes_active()
        sys_info = SystemInfoWidget()              
        sys_info.setParent(self.changes_active3_1)
        self.enable_mouse_events_recursive(sys_info)
        sys_info.show()
        self.changes_active3_1.show()
        
    def show_changes_active3_2(self):
        self.hide_changes_active()
        self.changes_active3_2.show()
        process_manager = ProcessManager()
        process_manager.setParent(self.changes_active3_2)
        self.enable_mouse_events_recursive(process_manager)
        process_manager.show()
        
    def show_changes_active4_1(self):
        self.hide_changes_active()
        self.changes_active4_1.show()
        sql_viewer = SQLViewer()
        sql_viewer.setParent(self.changes_active4_1)
        sql_viewer.show()
        
    def show_changes_active4_2(self):
        self.hide_changes_active()
        self.changes_active4_2.show()
        db_cheked = DBController()
        db_cheked.setParent(self.changes_active4_2)
        db_cheked.show()
        
        
    def show_changes_active5_2(self):
        self.hide_changes_active()
        self.changes_active5_2.show()
        pdf_viewer1 = PDFWidget1()
        pdf_viewer1.setParent(self.changes_active5_2)
        pdf_viewer1.show()
        
    def show_changes_active5_4(self):
        self.hide_changes_active()
        self.changes_active5_4.show()
        pdf_viewer2 = PDFWidget2()
        pdf_viewer2.setParent(self.changes_active5_4)
        pdf_viewer2.show()
        
    def save_session(self):
        settings = QSettings('config.ini', QSettings.IniFormat)
        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('windowState', self.saveState())
    
    def restore_session(self):
        settings = QSettings('config.ini', QSettings.IniFormat)
        self.restoreGeometry(settings.value('geometry'))
        self.restoreState(settings.value('windowState'))
    
    def open_activity(self):
        subprocess.Popen(['python', 'db_activity.py'])
        subprocess.Popen(['python', 'network_activity.py'])

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "SAM",
            "Приложение продолжает работать в трее.",
            QSystemTrayIcon.Information,
            2000
        )
    
    def create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("admin_icon.png"))
        self.tray_icon.setVisible(True)
        tray_menu = QMenu(self)
        restore_action = QAction("Открыть", self)
        quit_action = QAction("Выход", self)
        restore_action.triggered.connect(self.show)
        quit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(restore_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
    
        

if __name__ == '__main__':
    import sys
    
    app = QApplication(sys.argv)
    window = AdminTools()
    window.create_tray_icon()
    window.restore_session()
    window.open_activity()
    sys.exit(app.exec_())
