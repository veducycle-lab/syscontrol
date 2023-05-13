import sys
from PyQt5.QtCore import *
from PyQt5.QtNetwork import *

class Server(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Создаем серверный сокет
        self.server = QTcpServer(self)

        # Связываем серверный сокет с портом и адресом
        if not self.server.listen(QHostAddress("127.0.0.1"), 9999):
            print("Could not start server")
            sys.exit(1)

        # Соединяем сигнал нового клиента со слотом обработки нового клиента
        self.server.newConnection.connect(self.handle_new_connection)
        print("Server started")

    @pyqtSlot()
    def handle_new_connection(self):
        # Получаем новое соединение
        client_socket = self.server.nextPendingConnection()

        # Соединяем сигнал готовности данных для чтения со слотом чтения данных
        client_socket.readyRead.connect(self.handle_ready_read)

        print("New client connected")

    @pyqtSlot()
    def handle_ready_read(self):
        # Получаем сокет, из которого пришли данные
        client_socket = self.sender()

        # Читаем данные из сокета
        data = client_socket.readAll()

        # Отправляем обратно клиенту те же данные
        client_socket.write(data)

        print(f"Received '{data}' from client")

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)

    # Создаем сервер и запускаем цикл обработки событий
    server = Server()
    sys.exit(app.exec_())
