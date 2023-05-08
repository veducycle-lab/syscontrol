from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Создаем кнопку
        self.btn = QPushButton("Кнопка")

        # Создаем виджеты
        self.widget1 = QWidget()
        self.widget2 = QWidget()

        # Задаем текст виджетов
        self.widget1_text = "Это виджет 1"
        self.widget2_text = "Это виджет 2"

        # Создаем метки для виджетов и задаем им начальное значение
        self.widget1_lbl = QLabel(self.widget1_text)
        self.widget2_lbl = QLabel(self.widget2_text)

        # Создаем вертикальный компоновщик
        self.layout = QVBoxLayout()

        # Добавляем метки в виджеты
        self.widget1.setLayout(self.layout.addWidget(self.widget1_lbl))
        self.widget2.setLayout(self.layout.addWidget(self.widget2_lbl))

        # Устанавливаем начальное значение виджетов
        self.widget1_lbl.setText(self.widget1_text)
        self.widget2_lbl.setText(self.widget2_text)

        # При наведении курсора на кнопку меняем текст второго виджета
        self.btn.clicked.connect(self.on_btn_click)

        # Добавляем кнопку и виджеты в компоновщик
        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.widget1)
        self.layout.addWidget(self.widget2)

        # Устанавливаем компоновщик на окно
        self.setLayout(self.layout)

    def on_btn_click(self):
        self.widget2_lbl.setText("Новый текст второго виджета")

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
