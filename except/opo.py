import psutil
from PyQt5.QtWidgets import QApplication, QTreeWidgetItem, QTreeWidget, QMainWindow, QMenu, QAction, qApp
import sys
import os
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QLineEdit, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

class ProcessManager(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle("Process Monitor")
        # Создаем дерево для отображения процессов
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Name", "ID", "Status", "CPU %", "Memory %"])
        self.setCentralWidget(self.tree)

        # Создаем контекстное меню для дерева
        self.context_menu = QMenu(self.tree)
        kill_action = QAction("Kill", self)
        kill_action.triggered.connect(self.kill_process)
        self.context_menu.addAction(kill_action)
        self.tree.setSortingEnabled(True)
        self.tree.sortByColumn(0, Qt.AscendingOrder)

        # Настройка виджета строки поиска
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search...")
        self.search_box.textChanged.connect(self.search_processes)

        # Создаем словарь для хранения процессов
        self.processes_dict = {}

        # Устанавливаем интервал обновления списка процессов в миллисекундах
        self.update_interval = 1000

        # Запускаем таймер обновления процессов
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_processes)
        self.timer.start(self.update_interval)
        
        # Настройка главного виджета
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.search_box)
        layout.addWidget(self.tree)
        self.setCentralWidget(central_widget)

    def create_item(self, process):
        # Создаем элемент дерева для процесса
        if process.status() == psutil.STATUS_DEAD:
    # Удаленные объекты (красный)
            brush_color = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        elif process.username() == os.getlogin():
            # Собственные процессы (светло-голубой)
            brush_color = QtGui.QBrush(QtGui.QColor(135, 206, 250))
        elif process.status() == psutil.STATUS_STOPPED:
            # Приостановленные процессы (темно-серый)
            brush_color = QtGui.QBrush(QtGui.QColor(70, 70, 70))
        elif process.status() == psutil.STATUS_IDLE:
            # Упакованные образы (фиолетовый)
            brush_color = QtGui.QBrush(QtGui.QColor(153, 50, 204))
        # elif process.name() in psutil.WINDOWS_SERVICE_EXCEPTIONS:
        #     # Службы (светло-розовый)
        #     brush_color = QtGui.QBrush(QtGui.QColor(255, 192, 203))
        else:
            # Новые объекты (ярко-зеленый)
            brush_color = QtGui.QBrush(QtGui.QColor(0, 0, 0))

        item = QTreeWidgetItem([process.info['name'], str(process.info['pid']), process.info['status'], str(process.info['cpu_percent']), str(process.info['memory_percent'])])
        
        # Добавляем элемент в словарь процессов
        item.setForeground(0, brush_color)
        item.setForeground(1, brush_color)
        item.setForeground(2, brush_color)
        item.setForeground(3, brush_color)
        item.setForeground(4, brush_color)
        self.processes_dict[process.info['pid']] = item
        return item

    def update_processes(self):
        # Получаем информацию о процессах
        processes = psutil.process_iter(attrs=['pid', 'name', 'status', 'cpu_percent', 'memory_percent'])

        # Обновляем информацию о процессах в дереве
        for process in processes:
            pid = process.info['pid']
            if pid in self.processes_dict:
                # Процесс уже есть в словаре - обновляем информацию о нем
                item = self.processes_dict[pid]
                item.setText(2, process.info['status'])
                item.setText(3, str(process.info['cpu_percent']))
                item.setText(4, str(process.info['memory_percent']))
            else:
                # Процесса еще нет в словаре - добавляем его в дерево и словарь
                parent_pid = process.parent().pid if process.parent() else None
                if parent_pid in self.processes_dict:
                    parent_item = self.processes_dict[parent_pid]
                    parent_item.addChild(self.create_item(process))
                else:
                    self.tree.addTopLevelItem(self.create_item(process))

    def kill_process(self):
        # Получаем выбранный элемент дерева
        selected_item = self.tree.currentItem()

        # Получаем PID процесса из элемента дерева
        pid = int(selected_item.text(1))

        # Убиваем процесс
        process = psutil.Process(pid)
        process.terminate()

        # Удаляем элемент дерева
        selected_item.parent().removeChild(selected_item)

    def contextMenuEvent(self, event):
        # Отображаем контекстное меню для элемента дерева
        self.context_menu.exec_(event.globalPos())
    
    def search_processes(self, text):
        # Поиск процессов
        matches = self.tree.findItems(text, Qt.MatchContains | Qt.MatchRecursive, 0)

        # Установка видимости элементов
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            if item.text(0).lower().startswith(text.lower()):
                item.setHidden(False)
            else:
                item.setHidden(True)
        for item in matches:
            item.setHidden(False)    

if __name__ == "__main__":
    app = QApplication([])
    window = ProcessManager()
    window.show()
    app.exec_()
