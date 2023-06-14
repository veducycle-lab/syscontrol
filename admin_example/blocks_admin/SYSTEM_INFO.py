import sys
import psutil
import platform
import subprocess
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, QProgressBar
from PyQt5.QtCore import QTimer
import time
from collections import deque

class CPUWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.figure, self.ax = plt.subplots()
        self.chart_canvas = FigureCanvas(self.figure)
        self.chart_canvas.setMinimumSize(300, 200)

        self.label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.chart_canvas)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.cpu_percent = deque(maxlen=100)
        self.deque_timestamp = deque(maxlen=100)
        self.graph_lim = 50

        self.update_data()

    def update_data(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        self.cpu_percent.append(cpu_percent)
        self.deque_timestamp.append(time.time())

        self.ax.plot(list(self.deque_timestamp), list(self.cpu_percent), color='blue')
        self.ax.set_title('Использование процессора')

        if len(self.deque_timestamp) > 1:
            self.ax.set_xlim(min(self.deque_timestamp), max(self.deque_timestamp))
            self.ax.set_ylim(min(self.cpu_percent), max(self.cpu_percent))

        self.figure.canvas.draw()

        self.label.setText(f'Свободно: {100 - cpu_percent}%\nЗанято: {cpu_percent}%')

        QTimer.singleShot(1000, self.update_data)


class RAMWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.figure, self.ax = plt.subplots()
        self.chart_canvas = FigureCanvas(self.figure)
        self.chart_canvas.setMinimumSize(300, 200)

        self.label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.chart_canvas)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.ram_percent = deque(maxlen=100)
        self.deque_timestamp = deque(maxlen=100)
        self.graph_lim = 50

        self.update_data()

    def update_data(self):
        mem = psutil.virtual_memory()
        ram_percent = mem.percent
        self.ram_percent.append(ram_percent)
        self.deque_timestamp.append(time.time())

        self.ax.plot(list(self.deque_timestamp), list(self.ram_percent), color='orange')
        self.ax.set_title('Использование памяти')

        if len(self.deque_timestamp) > 1:
            self.ax.set_xlim(min(self.deque_timestamp), max(self.deque_timestamp))
            self.ax.set_ylim(min(self.ram_percent), max(self.ram_percent))

        self.figure.canvas.draw()

        self.label.setText(f'Свободно: {100 - ram_percent}%\nЗанято: {ram_percent}%')

        QTimer.singleShot(1000, self.update_data)


class DiskWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.disk_widgets = []
        self.disk_labels = []

        partitions = psutil.disk_partitions()
        colors = ['orange', 'cyan', 'green', 'red']
        for i, partition in enumerate(partitions):
            disk_widget = QProgressBar()
            disk_widget.setTextVisible(True)
            disk_widget.setRange(0, 100)

            disk_label = QLabel(partition.device)

            disk_widget.setStyleSheet(f"QProgressBar::chunk {{ background-color: {colors[i]}; }}")

            self.layout.addWidget(disk_label)
            self.layout.addWidget(disk_widget)

            self.disk_widgets.append(disk_widget)
            self.disk_labels.append(disk_label)

        self.setLayout(self.layout)

        self.update_data()

    def update_data(self):
        partitions = psutil.disk_partitions()
        for i, partition in enumerate(partitions):
            disk_widget = self.disk_widgets[i]
            disk_label = self.disk_labels[i]

            disk_usage = psutil.disk_usage(partition.mountpoint)
            total = disk_usage.total
            used = disk_usage.used
            used_percent = int(used / total * 100)

            disk_widget.setValue(used_percent)

            disk_widget.setFormat(f"  Used: {used} / {total} bytes ({used_percent}%)")

        QTimer.singleShot(1000, self.update_data)



class SystemInfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()

        self.cpu_widget = CPUWidget()
        self.ram_widget = RAMWidget()
        self.disk_widget = DiskWidget()

        self.system_info_labels = {
            "Информация о системе:": QLabel(),
            "Memory:": QLabel(),
            "Cpu:": QLabel(),
            "Disk:": QLabel(),
            "Hostname:": QLabel(),
            "Platform:": QLabel(),
            "Platform-version:": QLabel(),
            "Platform-release:": QLabel(),
            "RAM:": QLabel(),
            "Processor:": QLabel(),
            "CPU-Cores:": QLabel(),
            "Ip-address:": QLabel(),
            "Mac-address:": QLabel()
        }

        widget1 = QWidget()
        layout1 = QVBoxLayout()
        layout1.addWidget(self.cpu_widget)
        layout1.addWidget(self.ram_widget)
        layout1.addWidget(self.disk_widget)
        widget1.setLayout(layout1)

        widget2 = QWidget()
        layout2 = QGridLayout()
        row = 0
        for label_text, label in self.system_info_labels.items():
            layout2.addWidget(QLabel(label_text), row, 0)
            layout2.addWidget(label, row, 1)
            row += 1
        widget2.setLayout(layout2)

        self.layout.addWidget(widget1, 0, 0, 1, 1)
        self.layout.addWidget(widget2, 0, 1, 1, 1)

        self.setLayout(self.layout)

        self.resize(1901, 911)
        self.update_info()

    def update_info(self):
        self.cpu_widget.update_data()
        self.ram_widget.update_data()
        self.disk_widget.update_data()

        self.update_system_info()

    def update_system_info(self):
        mem = psutil.virtual_memory()
        self.system_info_labels["Memory:"].setText(f"{mem.total // (1024**3)} GB")
        self.system_info_labels["Cpu:"].setText(f"{platform.processor()}")

        # Очищаем предыдущую информацию о дисках
        self.system_info_labels["Disk:"].clear()

        # Получаем информацию о дисках
        disk_info = [f"{partition.device}: {psutil.disk_usage(partition.mountpoint).percent}%" for partition in psutil.disk_partitions()]
        disk_info_text = '\n'.join(disk_info)

        # Устанавливаем новое значение информации о дисках
        self.system_info_labels["Disk:"].setText(f"\n{disk_info_text}")

        self.system_info_labels["Hostname:"].setText(f"{platform.node()}")
        self.system_info_labels["Platform:"].setText(f"{platform.system()}")
        self.system_info_labels["Platform-version:"].setText(f"{platform.version()}")
        self.system_info_labels["Platform-release:"].setText(f"{platform.release()}")

        self.system_info_labels["RAM:"].setText(f"{mem.total // (1024**3)} GB")
        self.system_info_labels["Processor:"].setText(f"{platform.processor()}")
        self.system_info_labels["CPU-Cores:"].setText(f"{psutil.cpu_count(logical=False)}")

        addresses = psutil.net_if_addrs()
        
        if "Ethernet" in addresses:
            self.system_info_labels["Ip-address:"].setText(f"{addresses['Ethernet'][1].address}")
            self.system_info_labels["Mac-address:"].setText(f"{addresses['Ethernet'][0].address}")
        elif "Wi-Fi" in addresses:
            self.system_info_labels["Ip-address:"].setText(f"{addresses['Wi-Fi'][1].address}")
            self.system_info_labels["Mac-address:"].setText(f"{addresses['Wi-Fi'][0].address}")

        QTimer.singleShot(1000, self.update_system_info)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = SystemInfoWidget()
    widget.show()
    sys.exit(app.exec_())
