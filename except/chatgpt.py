import sys
import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout

class TaskManager(QWidget):
    def __init__(self):
        super().__init__()

        # set the window title and size
        self.setWindowTitle('Task Manager')
        self.setGeometry(100, 100, 800, 600)

        # create the GUI elements
        self.label = QLabel('Processes:', self)
        self.table = QTableWidget(self)
        self.button_end_task = QPushButton('End task', self)
        self.button_refresh = QPushButton('Refresh', self)

        # set the layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.table)
        self.layout.addStretch()
        self.layout.addLayout(self.create_button_layout())
        self.setLayout(self.layout)

        # create the initial process list
        self.create_table()

    def create_table(self):
        # set the table headers
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Name', 'PID', 'Status', 'CPU', 'Memory'])

        # get the list of running processes
        processes = []
        for proc in psutil.process_iter(['name', 'pid', 'status', 'cpu_percent', 'memory_percent']):
            processes.append(proc.info)

        # populate the table with the process data
        self.table.setRowCount(len(processes))
        for row, process in enumerate(processes):
            self.table.setItem(row, 0, QTableWidgetItem(process['name']))
            self.table.setItem(row, 1, QTableWidgetItem(str(process['pid'])))
            self.table.setItem(row, 2, QTableWidgetItem(process['status']))
            self.table.setItem(row, 3, QTableWidgetItem(f"{process['cpu_percent']:.2f}%"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{process['memory_percent']:.2f}%"))

    def update_table(self):
        # clear the table and create a new one
        self.table.clear()
        self.create_table()

    def end_task(self):
        # get the PID of the selected process
        row = self.table.currentRow()
        pid = int(self.table.item(row, 1).text())

        # end the process
        process = psutil.Process(pid)
        process.terminate()

        # update the process list
        self.update_table()

    def create_button_layout(self):
        # create the button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_end_task)
        button_layout.addStretch()
        button_layout.addWidget(self.button_refresh)

        # connect the buttons to their respective functions
        self.button_end_task.clicked.connect(self.end_task)
        self.button_refresh.clicked.connect(self.update_table)

        return button_layout

if __name__ == '__main__':
    app = QApplication(sys.argv)
    task_manager = TaskManager()
    task_manager.show()
    sys.exit(app.exec_())
