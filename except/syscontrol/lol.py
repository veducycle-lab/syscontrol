import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QLineEdit, QWidget, QLabel
from PyQt5.QtCore import Qt


class ProcessMonitor(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройка главного окна
        self.setWindowTitle("Process Monitor")
        self.resize(800, 600)

        # Настройка виджета дерева процессов
        self.tree = QTreeWidget()
        self.tree.setColumnCount(5)
        self.tree.setHeaderLabels(["Name", "ID", "Status", "CPU %", "Memory %"])
        self.tree.setSortingEnabled(True)
        self.tree.sortByColumn(0, Qt.AscendingOrder)

        # Настройка виджета строки поиска
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search...")
        self.search_box.textChanged.connect(self.search_processes)

        # Настройка главного виджета
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.search_box)
        layout.addWidget(self.tree)
        self.setCentralWidget(central_widget)

        # Получение списка процессов
        processes = {}
        for proc in psutil.process_iter(["pid", "name", "status", "cpu_percent", "memory_percent"]):
            if proc.ppid() not in processes:
                processes[proc.ppid()] = []
            processes[proc.ppid()].append((proc.pid, proc.name(), proc.status(), proc.cpu_percent(), proc.memory_percent()))

        # Очистка дерева и вставка процессов
        self.tree.clear()
        self.tree.setHeaderLabels(["Name", "ID", "Status", "CPU %", "Memory %"])
        root = QTreeWidgetItem(["System", "", "", "", ""])
        self.tree.addTopLevelItem(root)

        def add_processes(parent, processes):
            for process in sorted(processes, key=lambda x: x[1]):
                item = QTreeWidgetItem([process[1], str(process[0]), process[2], str(process[3]), str(process[4])])
                parent.addChild(item)
                if process[0] in processes:
                    add_processes(item, processes[process[0]])

        add_processes(root, processes.get(0, []))

        # Сортировка деревом
        self.tree.sortItems(0, Qt.AscendingOrder)

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
    monitor = ProcessMonitor()
    monitor.show()
    app.exec_()
