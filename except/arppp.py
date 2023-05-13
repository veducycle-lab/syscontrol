import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QProgressBar
from PyQt5.QtCore import Qt, QTimer
import os
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt RamMap")
        self.setGeometry(100, 100, 800, 400)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        self.verticalLayout = QVBoxLayout(centralWidget)

        self.memoryLabel = QLabel()
        self.memoryLabel.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.memoryLabel)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.valueChanged.connect(self.updateProgressBar)
        self.verticalLayout.addWidget(self.slider)

        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)
        self.progressBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.verticalLayout.addWidget(self.progressBar)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateMemoryUsage)
        self.timer.start(1000)

        self.updateMemoryUsage()

    def updateMemoryUsage(self):
        total, used, free = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
        memoryUsage = used / total * 100
        self.memoryLabel.setText("Memory Usage: {:.2f}%".format(memoryUsage))
        self.slider.setValue(memoryUsage)

    def updateProgressBar(self, value):
        self.progressBar.setValue(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
