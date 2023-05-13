import psutil
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
class ProcessMonitor(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создание главного окна
        self.setWindowTitle("Process Monitor")
        self.setGeometry(100, 100, 800, 600)

        # Создание таблицы
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Status", "CPU %", "Memory %"])
        self.setCentralWidget(self.table)

        # Обновление списка процессов каждые 2 секунды
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_processes)
        self.timer.start(2000)

        # Обновление списка процессов при запуске программы
        self.update_processes()
    def update_processes(self):
        # Получение списка процессов
        processes = []
        for proc in psutil.process_iter():
            try:
                processes.append((proc.pid, proc.name(), proc.status(), proc.cpu_percent(), proc.memory_percent()))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Очистка таблицы и вставка процессов
        self.table.setRowCount(len(processes))
        for row, proc in enumerate(processes):
            for col, value in enumerate(proc):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight if col in (0, 3, 4) else Qt.AlignVCenter | Qt.AlignLeft)
                self.table.setItem(row, col, item)
if __name__ == "__main__":
    app = QApplication([])
    monitor = ProcessMonitor()
    monitor.show()
    app.exec()
