import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *

class Client(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Создаем клиентский сокет
        self.socket = QTcpSocket(self)

        # Создаем виджеты
        self.label = QLabel("Waiting for connection...")
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        # Создаем компоновщик
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

        # Соединяем сигналы со слотами
        self.socket.connected.connect(self.handle_connected)
        self.socket.disconnected.connect(self.handle_disconnected)
        self.socket.readyRead.connect(self.handle_ready_read)

        # Создаем таймер для проверки подключения
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_server)
        self.timer.start(1000)

    def check_server(self):
        if self.socket.state() == QAbstractSocket.UnconnectedState:
            self.label.setText("Connecting to server...")
            self.socket.connectToHost("127.0.0.1", 9999)

    @pyqtSlot()
    def handle_connected(self):
        self.label.setText("Connected to server")
        self.text_edit.append("Connected to server")

    @pyqtSlot()
    def handle_disconnected(self):
        self.label.setText("Disconnected from server")
        self.text_edit.append("Disconnected from server")

    @pyqtSlot()
    def handle_ready_read(self):
        data = self.socket.readAll().data().decode()
        self.text_edit.append(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Создаем окно и запускаем приложение
    client = Client()
    client.show()
    sys.exit(app.exec_())
