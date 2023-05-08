import psutil
from PyQt5 import QtWidgets, QtCore

class ProcessMonitor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        # Создаем компоненты интерфейса
        self.process_list = QtWidgets.QListWidget()
        self.cpu_usage_label = QtWidgets.QLabel()
        self.memory_usage_label = QtWidgets.QLabel()
        self.disk_usage_label = QtWidgets.QLabel()
        self.network_usage_label = QtWidgets.QLabel()
        self.refresh_button = QtWidgets.QPushButton('Обновить')
        self.kill_button = QtWidgets.QPushButton('Снять задачу')
        
        # Создаем вертикальный слой для компонентов интерфейса
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.process_list)
        vbox.addWidget(self.cpu_usage_label)
        vbox.addWidget(self.memory_usage_label)
        vbox.addWidget(self.disk_usage_label)
        vbox.addWidget(self.network_usage_label)
        vbox.addWidget(self.refresh_button)
        vbox.addWidget(self.kill_button)
        self.setLayout(vbox)
        
        # Устанавливаем обработчики событий
        self.refresh_button.clicked.connect(self.refresh_processes)
        self.kill_button.clicked.connect(self.kill_selected_process)
        
        # Запускаем таймер для обновления информации о процессах в реальном времени
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.refresh_processes)
        self.timer.start(1000)
        
        # Обновляем информацию о процессах при запуске приложения
        self.refresh_processes()
        
    def refresh_processes(self):
        self.process_list.clear()
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            self.process_list.addItem(f"{proc.info['pid']} {proc.info['name']} {proc.info['cpu_percent']}% {proc.info['memory_percent']}%")
            
        cpu_usage = psutil.cpu_percent(interval=None)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        network_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        self.cpu_usage_label.setText(f"Использование ЦП: {cpu_usage}%")
        self.memory_usage_label.setText(f"Использование памяти: {memory_usage}%")
        self.disk_usage_label.setText(f"Использование диска: {disk_usage}%")
        self.network_usage_label.setText(f"Использование сети: {network_usage / 1024 / 1024} MB")
        
    def kill_selected_process(self):
        selected_items = self.process_list.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            pid = int(selected_item.text().split()[0])
            proc = psutil.Process(pid)
            proc.kill()
            self.refresh_processes()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    monitor = ProcessMonitor()
    monitor.show()
    app.exec_()
