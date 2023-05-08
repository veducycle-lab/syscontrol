from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFrame, QVBoxLayout, QHBoxLayout

class MyWindow(QWidget): 
    def __init__(self): 
        super().__init__()
        # Создаем фреймы
        self.frame1 = QFrame()
        self.frame2 = QFrame()

        # Задаем цвета фреймов
        self.frame1.setStyleSheet("background-color: red")
        self.frame2.setStyleSheet("background-color: white")

        # Создаем кнопки
        self.button1 = QPushButton("Фрейм 1")
        self.button2 = QPushButton("Фрейм 2")

        # При нажатии на кнопки меняем текущий виджет на соответствующий фрейм
        self.button1.clicked.connect(lambda:self.set_current_frame(1))
        self.button2.clicked.connect(lambda:self.set_current_frame(2))

        # Создаем вертикальный компоновщик для кнопок
        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.button1)
        self.button_layout.addWidget(self.button2)

        # Создаем горизонтальный компоновщик для фреймов и кнопок
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.frame1)
        self.main_layout.addWidget(self.frame2)
        self.main_layout.addLayout(self.button_layout)

        # Устанавливаем начальный видимый фрейм
        self.current_frame = self.frame1

        # Устанавливаем компоновщик на окно
        self.setLayout(self.main_layout)

    def set_current_frame(self, frame_num):
        if frame_num == 1:
            self.current_frame = self.frame1
        elif frame_num == 2:
            self.current_frame = self.frame2
        self.current_frame.show()
        for frame in [self.frame1, self.frame2]:
            if frame != self.current_frame:
                frame.hide()

if __name__ == "__main__": 
    app = QApplication([]) 
    window = MyWindow() 
    window.show() 
    app.exec_()                