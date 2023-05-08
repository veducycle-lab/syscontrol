from PyQt5.QtWidgets import QMainWindow, QFrame, QPushButton, QStackedWidget, QLabel, QVBoxLayout, QWidget, QApplication
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import Qt
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # main window properties
        self.setGeometry(500, 500, 900, 150)
        self.setWindowTitle('SysControl')
        self.setWindowIcon(QIcon(""))


        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: blue;
                text-decoration: underline;
            }
                QPushButton:hover {
                background-color: #fff;
                color: #3498db;
            }
                QPushButton:hover {
                background-color: #fff;
                color: #3498db;
            }
        """)
        # self.showFullScreen()

        # Создаем QStackedWidget и добавляем в него два лейбла
        self.stacked_widget = QStackedWidget()
        self.label1 = QLabel("Первый лейбл")
        self.label2 = QLabel("Второй лейбл")
        self.stacked_widget.addWidget(self.label1)
        self.stacked_widget.addWidget(self.label2)

        # Создаем кнопки для переключения между лейблами
        self.button1 = QPushButton("Перейти к лейблу 1")
        self.button1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.button1.setFlat(True)  # убираем границы кнопки
        
        self.button2 = QPushButton("Перейти к лейблу 2")
        self.button2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.button2.setFlat(True)  # убираем границы кнопки
        

        # Создаем вертикальный макет и добавляем в него кнопки и QStackedWidget
        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.stacked_widget)

        widget = QWidget()
        widget.setLayout(layout)

        # Устанавливаем виджет в качестве центрального виджета главного окна
        self.setCentralWidget(widget)


        

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()