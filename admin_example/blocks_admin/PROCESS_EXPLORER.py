import psutil
import os
from PyQt5.QtWidgets import QApplication, QTreeWidgetItem, QTreeWidget, QMainWindow, QMenu, QAction, qApp, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLineEdit, QWidget
from PyQt5 import QtGui


class ProcessManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Process Monitor")
        self.resize(1901, 911)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Name", "ID", "Status", "CPU %", "Memory %"])

        self.context_menu = QMenu(self.tree)
        kill_action = QAction("Kill", self)
        kill_action.triggered.connect(self.kill_process)
        info_action = QAction("Info", self)
        info_action.triggered.connect(self.show_process_info)
        self.context_menu.addAction(info_action)
        self.context_menu.addAction(kill_action)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search...")
        self.search_box.textChanged.connect(self.search_processes)

        self.processes_dict = {}
        self.update_interval = 2600
        self.iteration_count = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_processes)
        self.timer.start(self.update_interval)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.search_box)
        layout.addWidget(self.tree)
        self.setCentralWidget(central_widget)

    def create_item(self, process):
        pid = process.info['pid']
        if pid in self.processes_dict:
            # Return the existing item if it already exists
            return self.processes_dict[pid]
        else:
            item = QTreeWidgetItem([process.info['name'], str(pid),
                                    process.info['status'], str(process.info['cpu_percent']),
                                    str(process.info['memory_percent'])])

            item.setForeground(0, QtGui.QBrush(QtGui.QColor(0, 0, 0)))
            item.setForeground(1, QtGui.QBrush(QtGui.QColor(0, 0, 0)))
            item.setForeground(2, QtGui.QBrush(QtGui.QColor(0, 0, 0)))
            item.setForeground(3, QtGui.QBrush(QtGui.QColor(0, 0, 0)))
            item.setForeground(4, QtGui.QBrush(QtGui.QColor(0, 0, 0)))

            company_name = process.info.get('company_name', '')
            if company_name.lower().startswith('microsoft'):
                item.setForeground(0, QtGui.QBrush(QtGui.QColor(0, 0, 255)))
                item.setForeground(1, QtGui.QBrush(QtGui.QColor(0, 0, 255)))
                item.setForeground(2, QtGui.QBrush(QtGui.QColor(0, 0, 255)))
                item.setForeground(3, QtGui.QBrush(QtGui.QColor(0, 0, 255)))
                item.setForeground(4, QtGui.QBrush(QtGui.QColor(0, 0, 255)))


            # Add the item to the processes_dict
            self.processes_dict[pid] = item

            return item


    def update_processes(self):
        processes = psutil.process_iter(attrs=['pid', 'name', 'status', 'cpu_percent', 'memory_percent'])
        processes_to_remove = []
        for process in processes:
            pid = process.info['pid']
            if pid in self.processes_dict:
                item = self.processes_dict[pid]
                item.setText(2, process.info['status'])
                item.setText(3, str(process.info['cpu_percent']))
                item.setText(4, str(process.info['memory_percent']))

                if process.status() == psutil.STATUS_DEAD or (process.parent() and process.parent().pid == os.getpid()):
                    processes_to_remove.append(pid)
            else:
                parent_pid = process.parent().pid if process.parent() else None
                if parent_pid in self.processes_dict:
                    parent_item = self.processes_dict[parent_pid]
                    parent_item.addChild(self.create_item(process))
                else:
                    item = self.create_item(process)
                    self.tree.addTopLevelItem(item)
                    self.processes_dict[pid] = item
                    
                    if self.iteration_count <= 1:
                        item.setBackground(0, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
                        item.setBackground(1, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
                        item.setBackground(2, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
                        item.setBackground(3, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
                        item.setBackground(4, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
                    elif process.status() == psutil.STATUS_RUNNING or process.status() == psutil.STATUS_SLEEPING:
                        item.setBackground(0, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
                        item.setBackground(1, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
                        item.setBackground(2, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
                        item.setBackground(3, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
                        item.setBackground(4, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
                
                    elif process.info.get('company_name', '').lower().startswith('Microsoft'):
                        item.setBackground(0, QtGui.QBrush(QtGui.QColor(0, 0, 255)))
                        item.setBackground(1, QtGui.QBrush(QtGui.QColor(0, 0, 255)))
                        item.setBackground(2, QtGui.QBrush(QtGui.QColor(0, 0, 255)))
                        item.setBackground(3, QtGui.QBrush(QtGui.QColor(0, 0, 255)))
                        item.setBackground(4, QtGui.QBrush(QtGui.QColor(0, 0, 255)))
                    elif process.username() == os.getlogin():
                        item.setBackground(0, QtGui.QBrush(QtGui.QColor(135, 206, 250)))
                        item.setBackground(1, QtGui.QBrush(QtGui.QColor(135, 206, 250)))
                        item.setBackground(2, QtGui.QBrush(QtGui.QColor(135, 206, 250)))
                        item.setBackground(3, QtGui.QBrush(QtGui.QColor(135, 206, 250)))
                        item.setBackground(4, QtGui.QBrush(QtGui.QColor(135, 206, 250)))
                    else:
                        item.setBackground(0, QtGui.QBrush(QtGui.QColor(135, 206, 235)))
                        item.setBackground(1, QtGui.QBrush(QtGui.QColor(135, 206, 235)))
                        item.setBackground(2, QtGui.QBrush(QtGui.QColor(135, 206, 235)))
                        item.setBackground(3, QtGui.QBrush(QtGui.QColor(135, 206, 235)))
                        item.setBackground(4, QtGui.QBrush(QtGui.QColor(135, 206, 235)))
                
                    self.iteration_count += 1
            
            for pid in processes_to_remove:
                item = self.processes_dict.pop(pid)
                index = self.tree.indexOfTopLevelItem(item)
                self.tree.takeTopLevelItem(index)

    def kill_process(self):
        selected_item = self.tree.currentItem()
        pid = int(selected_item.text(1))
        process = psutil.Process(pid)
        process.terminate()
        
        # Загорание красным цветом на 2 итерации
        selected_item.setBackground(0, QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        selected_item.setBackground(1, QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        selected_item.setBackground(2, QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        selected_item.setBackground(3, QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        selected_item.setBackground(4, QtGui.QBrush(QtGui.QColor(255, 0, 0)))
        
        QTimer.singleShot(2 * self.update_interval, lambda: self.restore_background_color(selected_item))  # Восстановление цвета после 2 итераций

        del self.processes_dict[pid]
        self.tree.takeTopLevelItem(self.tree.indexOfTopLevelItem(selected_item))


    def remove_process(self, item):
        pid = int(item.text(1))
        del self.processes_dict[pid]
        parent = item.parent()
        if parent:
            parent.removeChild(item)
        else:
            index = self.tree.indexOfTopLevelItem(item)
            self.tree.takeTopLevelItem(index)
        item = None

    def restore_background_color(self, item):
        item.setBackground(0, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        item.setBackground(1, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        item.setBackground(2, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        item.setBackground(3, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        item.setBackground(4, QtGui.QBrush(QtGui.QColor(255, 255, 255)))

    def show_process_info(self):
        selected_item = self.tree.currentItem()
        pid = int(selected_item.text(1))
        process = psutil.Process(pid)
        info = f"Name: {process.name()}\n"\
        f"PID: {pid}\n"\
        f"Status: {process.status()}\n"\
        f"CPU %: {process.cpu_percent()}\n"\
        f"Memory %: {process.memory_percent()}"
        QMessageBox.information(self, "Process Info", info)

    def contextMenuEvent(self, event):
        self.context_menu.exec_(event.globalPos())

    def search_processes(self, text):
            matches = self.tree.findItems(text, Qt.MatchContains | Qt.MatchRecursive, 0)
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