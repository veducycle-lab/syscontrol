from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QPushButton
from PyQt5.QtGui import QColor
import psutil
from PyQt5.QtCore import Qt, QTimer
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Processes")
        self.tree = QTreeWidget(self)
        self.tree.setHeaderLabels(["Name", "PID", "Status"])
        self.tree.resize(800, 600)
        self.tree.move(0, 40)
        self.tree.setColumnWidth(0, 400)
        self.tree.setColumnWidth(1, 100)
        self.tree.setColumnWidth(2, 200)
        self.update_processes()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_processes)
        self.timer.start(2000)
        self.terminate_button = QPushButton("Terminate", self)
        self.terminate_button.move(700, 5)
        self.terminate_button.clicked.connect(self.terminate_process)

    def update_processes(self):
        existing_pids = []
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            pid = int(item.text(1))
            existing_pids.append(pid)
            try:
                p = psutil.Process(pid)
                if p.status() == psutil.STATUS_ZOMBIE:
                    item.setBackground(2, QColor("grey"))
                elif p.status() == psutil.STATUS_IDLE:
                    item.setBackground(2, QColor("lightgrey"))
                elif p.status() == psutil.STATUS_RUNNING:
                    if pid in self.new_pids:
                        item.setBackground(2, QColor("green"))
                    elif "Microsoft Company" in p.username():
                        item.setBackground(2, QColor("#FFC0CB"))
                    else:
                        item.setBackground(2, QColor("white"))
                elif p.status() == psutil.STATUS_STOPPED:
                    item.setBackground(2, QColor("red"))
                elif p.status() == psutil.STATUS_DEAD:
                    item.setBackground(2, QColor("darkred"))
            except psutil.NoSuchProcess:
                self.tree.takeTopLevelItem(i)
        self.new_pids = []
        for p in psutil.process_iter(attrs=["pid", "name", "username", "status"]):
            if p.info['pid'] not in existing_pids:
                self.new_pids.append(p.info['pid'])
                self.tree.addTopLevelItem(self.create_item(p.info))

    def create_item(self, process_info):
        item = QTreeWidgetItem()
        item.setText(0, process_info["name"])
        item.setText(1, str(process_info["pid"]))
        item.setText(2, process_info["status"])
        return item

    def terminate_process(self):
        for item in self.tree.selectedItems():
            pid = int(item.text(1))
            try:
                p = psutil.Process(pid)
                p.terminate()
                item.setBackground(2, QColor("red"))
            except psutil.NoSuchProcess:
                self.tree.takeTopLevelItem(self.tree.indexOfTopLevelItem(item))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
