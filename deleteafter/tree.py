from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QStackedWidget, QLabel

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Создаем QStackedWidget и добавляем в него 3 виджета
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(QWidget())
        self.stacked_widget.addWidget(QWidget())
        self.stacked_widget.addWidget(QWidget())
        
        # Создаем кнопки
        self.button_main = QPushButton("Главная")
        self.button_graphs = QPushButton("Графики")
        self.button_network = QPushButton("Сеть")
        
        # Создаем надпись расположения
        self.label_location = QLabel("Главная")

        # Объединяем кнопки в горизонтальный лайаут
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.button_main)
        buttons_layout.addWidget(self.button_graphs)
        buttons_layout.addWidget(self.button_network)

        # Объединяем кнопки и надпись расположения в вертикальный лайаут
        location_layout = QVBoxLayout()
        location_layout.addWidget(self.label_location)
        location_layout.addLayout(buttons_layout)

        # Объединяем QStackedWidget и лайаут расположения в горизонтальный лайаут, который будем использовать как центральный виджет окна
        center_layout = QHBoxLayout()
        center_layout.addWidget(self.stacked_widget)
        center_layout.addLayout(location_layout)

        # Присваиваем центральный лайаут виджету центрального окна
        self.central_widget.setLayout(center_layout)

        # Обработчики нажатий кнопок
        self.button_main.clicked.connect(lambda: self.change_location("Главная"))
        self.button_graphs.clicked.connect(lambda: self.change_location("Главная/Графики"))
        self.button_network.clicked.connect(lambda: self.change_location("Главная/Графики/Сеть"))

    def change_location(self, text):
        self.label_location.setText(text)
        index = text.count("/")
        self.stacked_widget.setCurrentIndex(index)
        
        
if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
