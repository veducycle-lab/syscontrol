import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt, QTimer

class ProcessMonitor(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создаем дерево процессов
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Name", "ID", "Status", "CPU %", "Memory %"])
        self.setCentralWidget(self.tree)

        # Обновляем информацию о процессах
        self.update_processes()

        # Создаем таймер и устанавливаем его интервал
        self.timer = QTimer()
        self.timer.setInterval(1000)

        # Подключаем обработчик события timeout таймера
        self.timer.timeout.connect(self.update_processes)

        # Запускаем таймер
        self.timer.start()

    def create_item(self, process):
        # Создаем элемент дерева процессов
        item = QTreeWidgetItem()
        item.setText(0, process.info['name'])
        item.setText(1, str(process.info['pid']))
        item.setText(2, process.info['status'])
        item.setText(3, str(process.info['cpu_percent']))
        item.setText(4, str(process.info['memory_percent']))
        return item

    def update_processes(self):
        # Получаем информацию о процессах
        processes = psutil.process_iter(attrs=['pid', 'name', 'status', 'cpu_percent', 'memory_percent'])

        # Обновляем информацию о процессах в дереве
        for process in processes:
            pid = str(process.info['pid'])
            item = self.tree.findItems(pid, Qt.MatchExactly, 1)
            if len(item) > 0:
                item[0].setText(2, process.info['status'])
                item[0].setText(3, str(process.info['cpu_percent']))
                item[0].setText(4, str(process.info['memory_percent']))
            else:
                parent_pid = str(process.parent().pid) if process.parent() else ""
                parent_item = self.tree.findItems(parent_pid, Qt.MatchExactly, 1)
                if len(parent_item) > 0:
                    parent_item[0].addChild(self.create_item(process))
                else:
                    self.tree.addTopLevelItem(self.create_item(process))

    def search_processes(self, query):
        # Ищем процессы по запросу
        for item in self.tree.findItems(query, Qt.MatchContains | Qt.MatchRecursive, 0):
            item.setExpanded(True)
            self.tree.setCurrentItem(item)

if __name__ == "__main__":
    app = QApplication([])
    monitor = ProcessMonitor()
    monitor.show()
    app.exec_()
