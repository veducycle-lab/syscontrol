import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QProgressBar
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QRect, Qt, QTimer
import timeit
import json
import socket
import psutil
import platform
import os
import subprocess

class InstallerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setFixedSize(605, 380)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.cancel = QPushButton(self.centralwidget)
        self.cancel.setObjectName("cancel")
        self.cancel.setGeometry(QRect(410, 310, 80, 24))
        self.cancel.clicked.connect(self.cancelClicked)
        self.cancel.setText("Отмена")
        self.future = QPushButton(self.centralwidget)
        self.future.setObjectName("future")
        self.future.setGeometry(QRect(510, 310, 80, 24))
        self.future.clicked.connect(self.futureClicked)
        self.future.setText("Далее")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.widget.setGeometry(QRect(10, 10, 581, 291))
        self.text_label = QLabel(self.widget)
        self.text_label.setGeometry(QRect(0, 0, 581, 241))
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setText("Добро пожаловать, это установщик самой\nлучшей и расширяемой мониторинговой системы\nSAM(SysAlphMonitor)")
        self.setCentralWidget(self.centralwidget)
        self.menubar = self.menuBar()
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 605, 21))
        self.setWindowTitle("SAM")
        self.setWindowIcon(QIcon("icon.png"))
        self.unpack_time = 0
        self.db_connection = sqlite3.connect("auth_keys.db")
        font = QFont("Arial", 18)
        self.text_label.setFont(font)
    
    def send_data_to_server(data):
        server_ip = "127.0.0.1" #ip локальный, потому что нету сайта который будет принимать данные
        server_port = 80
        json_data = json.dumps(data)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, server_port))
            s.sendall(json_data.encode())
            response = s.recv(1024)
            s.close()
        with open("data.json", "w") as file:
            file.write(json_data)
    
    def cancelClicked(self):
        self.close()
    
    def futureClicked(self):
        self.text_label.setText("Введите ключ активации:")
        self.input_lineedit = QLineEdit(self.widget)
        self.input_lineedit.setGeometry(QRect(145, 150, 300, 26))
        self.input_lineedit.show()
        self.future.clicked.disconnect()
        self.future.clicked.connect(self.nextClicked)
        self.future.setText("Далее")
        self.cancel.setText("Отмена")
    
    def nextClicked(self):
        activation_key = self.input_lineedit.text()
        auth_key_client = self.fetch_auth_key("auth_key_client")
        auth_key_admin = self.fetch_auth_key("auth_key_admin")
        self.future.setText("Далее")
        self.cancel.setText("Отмена")
        if activation_key == auth_key_client:
            self.preFinishedClickedClient()
        elif activation_key == auth_key_admin:
            self.preFinishedClickedAdmin()
        else:
            self.text_label.clear()
            self.text_label.setText("Вы не прошли проверку,\nваши данные отправлены в\nслужбу безопасности")
            self.cancel.hide()
            self.future.hide()
            data = {
                "ip_address": socket.gethostbyname(socket.gethostname()),
                "mac_address": ":".join(["{:02x}".format((psutil.net_if_addrs()['eth0'][0].address.split(":")))]),
                "serial_number": psutil.disk_partitions()[0].serial,
                "network": psutil.net_if_stats()['eth0'].speed,
                "platform_type": platform.system(),
                "platform_version": platform.version(),
                "computer_name": socket.gethostname(),
                "processor": platform.processor()
            }
            self.send_data_to_server(data)
        self.input_lineedit.hide()
    
    def preFinishedClickedClient(self):
        self.text_label.clear()
        self.text_label.setText("Вы прошли проверку как пользователь")
        self.cancel.hide()
        self.future.clicked.connect(self.FinishedClient)
        self.future.setText("Далее")
    
    def preFinishedClickedAdmin(self):
        self.text_label.clear()
        self.text_label.setText("Вы прошли проверку как админ")
        self.cancel.hide()
        self.future.clicked.connect(self.FinishedAdmin)
        self.future.setText("Далее")
    
    def FinishedClient(self):
        self.text_label.clear()
        self.text_label.setText("Производится установка")
        self.progress_bar = QProgressBar(self.widget)
        self.progress_bar.setGeometry(QRect(10, 60, 561, 23))
        self.progress_bar.setValue(0)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.show()
        self.future.setText("Готово")
        self.future.setEnabled(False)
        self.future.setStyleSheet("color: gray")
        self.future.clicked.connect(self.FinishedClient)
        unpack_time = self.unpackArchiveClient()
        self.animateProgressBar(unpack_time)
    
    def FinishedAdmin(self):
        self.text_label.clear()
        self.text_label.setText("Производится установка")
        self.progress_bar = QProgressBar(self.widget)
        self.progress_bar.setGeometry(QRect(10, 60, 561, 23))
        self.progress_bar.setValue(0)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.show()
        self.future.setText("Готово")
        self.future.setEnabled(False)
        self.future.setStyleSheet("color: gray")
        self.future.clicked.connect(self.FinishedAdmin)
        unpack_time = self.unpackArchiveAdmin()
        self.animateProgressBar(unpack_time)
    
    def animateProgressBar(self, unpack_time):
        interval = int(unpack_time * 100000 / 10)
        self.timer = QTimer()
        self.timer.setInterval(interval)
        self.timer.timeout.connect(self.updateProgressBar)
        self.timer.start()
    
    def unpackArchiveAdmin(self):
        primary_disk = os.getenv('SystemDrive', 'C:')
        program_files_folder = os.path.join(primary_disk, 'Program Files', 'SAM')
        os.makedirs(program_files_folder, exist_ok=True)
        setup_code = '''
import zipfile
import time
        '''
        unpack_code = f'''
with zipfile.ZipFile('PortablePy.zip', 'r') as zip_ref:
    zip_ref.extractall('{program_files_folder}')
with zipfile.ZipFile('admin_repo.zip', 'r') as zip_ref:
    zip_ref.extractall('{program_files_folder}')
    '''
        unpack_time = timeit.timeit(unpack_code, setup=setup_code, number=1)
        return unpack_time,program_files_folder
    
    def unpackArchiveClient(self):
        primary_disk = os.getenv('SystemDrive', 'C:')
        program_files_folder = os.path.join(primary_disk, 'Program Files', 'SAM')
        os.makedirs(program_files_folder, exist_ok=True)
        setup_code = '''
import zipfile
import time
        '''
        unpack_code = f'''
with zipfile.ZipFile('PortablePy.zip', 'r') as zip_ref:
    zip_ref.extractall('{program_files_folder}')
with zipfile.ZipFile('cleint_repo.zip', 'r') as zip_ref:
    zip_ref.extractall('{program_files_folder})
    '''
        unpack_time = timeit.timeit(unpack_code, setup=setup_code, number=1)
        return unpack_time,program_files_folder
    
    def updateProgressBar(self):
        value = self.progress_bar.value()
        value += 10
        self.progress_bar.setValue(value)
        if value >= 100:
            self.timer.stop()
            self.future.setEnabled(True)
            self.future.setStyleSheet("")
            self.text_label.clear()
            if self.sender() == self.future:
                self.text_label.setText("\nУстановка завершена.\nДобро пожаловать в сервис SAM.")
            else:
                self.text_label.setText("\nУстановка завершена.\nДобро пожаловать в сервис SAM.\nХорошего вам пользования.")
            self.future.setText("Готово")
            self.future.clicked.disconnect()
            if self.sender() == self.future:
                self.future.clicked.connect(self.openClient)
            else:
                self.future.clicked.connect(self.openAdmin)
    
    def openClient(self):
        program_files_folder = os.path.join(os.getenv('SystemDrive', 'C:'), 'Program Files', 'SAM')
        os.chdir(program_files_folder)
        subprocess.Popen(['Console-Launcher.exe', 'client_create_db.py'])
        subprocess.Popen(['Console-Launcher.exe', 'client_app.py'])
        self.close()
    
    def openAdmin(self):
        program_files_folder = os.path.join(os.getenv('SystemDrive', 'C:'), 'Program Files', 'SAM')
        os.chdir(program_files_folder)
        subprocess.Popen(['Console-Launcher.exe', 'admin_create_db.py'])
        subprocess.Popen(['Console-Launcher.exe', 'admin_app.py'])
        self.close()
    
    def fetch_auth_key(self, key_type):
        cursor = self.db_connection.cursor()
        cursor.execute(f"SELECT {key_type} FROM sys_key")
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result[0]
        else:
            return None
        