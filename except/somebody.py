from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QMessageBox
from somebody2 import MainWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.username_input = QLineEdit()
        self.username_input.editingFinished.connect(self.checkUsername)

    def initUI(self):
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Login')

        self.login_button = QPushButton('Войти', self)
        self.login_button.move(30, 90)
        self.login_button.clicked.connect(self.check_login)

        self.username_field = QLineEdit(self)
        self.username_field.move(30, 30)

        self.show()

    def check_login(self):
        username = self.username_field.text()
        # здесь можно добавить какую-то логику проверки
        if not username:
            QMessageBox.warning(self, 'Ошибка', 'Введите имя пользователя')
        else:
            self.show_main_window()

    def show_main_window(self):
        self.hide()
        # создаем и показываем следующее окно (замените это на ваше окно)
        self.main_window = MainWindow()
        self.main_window.show()
    
    def checkUsername(self):
        # your username validation logic here
        pass

if __name__ == '__main__':
    app = QApplication([])
    window = LoginWindow()
    app.exec_()

