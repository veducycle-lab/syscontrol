import sys
import sqlite3
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction, QDialog, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QWidget
import subprocess
import socket
import os
import datetime

class LoginPassword(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Напишите ваш логин и пароль")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Поле для ввода логина"))
        self.login_edit = QLineEdit()
        layout.addWidget(self.login_edit)
        layout.addWidget(QLabel("Поле для ввода пароля"))
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_edit)
        login_button = QPushButton("Логин")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)
        self.setLayout(layout)

    def login(self):
        login = self.login_edit.text()
        password = self.password_edit.text()
        if check_credentials(login, password):
            self.accept()
        else:
            self.login_edit.clear()
            self.password_edit.clear()
            self.login_edit.setFocus()
            self.error_label.setText("Неверно введен логин и пароль")


class MainApp(QMainWindow):
    def __init__(self, id_person):
        super().__init__()
        self.setWindowTitle("Главное окно")
        self.setCentralWidget(QLabel("Привет, я QMainWindow!"))
        layout = QVBoxLayout()
        self.problem_label = QLabel("Если у вас возникли проблемы с использованием ПК, опишите проблему:")
        self.problem_label.setFont(QtGui.QFont("Arial", 16))
        layout.addWidget(self.problem_label)
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)
        self.send_button = QPushButton("Отправить")
        self.send_button.clicked.connect(self.send_problem)
        layout.addWidget(self.send_button)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.id_person = id_person


        self.start_activity()

    def start_activity(self):
        program_files_folder = os.path.join(os.getenv('SystemDrive', 'C:'), 'Program Files', 'SAM')
        os.chdir(program_files_folder)
        activity_process = subprocess.Popen(['Console-Launcher.exe', "send_me.py"])
        other_process = subprocess.Popen(['Console-Launcher.exe', "send_activity.py"])
        self.activity_process = activity_process
        self.other_process = other_process

    def closeEvent(self, event):
        # Закрытие activity.py и другого файла.py при закрытии основного окна
        if self.activity_process:
            self.activity_process.terminate()
            self.activity_process.wait()
        if self.other_process:
            self.other_process.terminate()
            self.other_process.wait()
        event.accept()

    def send_problem(self):
        problem_text = self.text_edit.toPlainText()
        ip_server = get_server_ip()
        if ip_server:
            for port in range(25678, 25980):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try:
                        s.connect((ip_server, port))
                        conn = sqlite3.connect("server_control.db")
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO problems (id_pc, id_person, problem) VALUES (?, ?, ?)", (1, self.id_person, problem_text))
                        conn.commit()
                        conn.close()
                        dialog = QDialog()
                        dialog.setWindowTitle("Успешно отправлено")
                        layout = QVBoxLayout()
                        layout.addWidget(QLabel("Ваша жалоба отправлена системному администратору."))
                        dialog.setLayout(layout)
                        dialog.exec_()
                        return
                    except ConnectionRefusedError:
                        pass

    def create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon("client_icon.png"))
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()

        tray_menu = QMenu()
        open_action = QAction("Открыть приложение", self)
        open_action.triggered.connect(self.show)
        tray_menu.addAction(open_action)
        quit_action = QAction("Выход", self)
        quit_action.triggered.connect(app.quit)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()


def get_server_ip():
    conn = sqlite3.connect("local_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT ip_server FROM server_recover")
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None


def check_credentials(login, password):
    ip_server = get_server_ip()
    if ip_server:
        for port in range(25678, 25980):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.connect((ip_server, port))
                    conn = sqlite3.connect("persons.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT id_person, login, psswd FROM person_login_psswd WHERE login = ? AND psswd = ?", (login, password))
                    result = cursor.fetchone()
                    conn.close()
                    return result is not None
                except ConnectionRefusedError:
                    pass
    return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    login_dialog = LoginPassword()
    if login_dialog.exec_() == QDialog.Accepted:
        id_person = login_dialog.result()
        if id_person is not None:
            window = MainApp(id_person)
            window.create_tray_icon()
            window.show()
            sys.exit(app.exec_())
