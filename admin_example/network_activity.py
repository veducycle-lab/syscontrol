import sqlite3
import socket

# Функция для сканирования ethernet порта и добавления информации о роутерах в базу данных
def scan_ethernet_port():
    # Определите номер ethernet порта, который нужно сканировать
    ethernet_port = 12345

    # Создайте соединение с базой данных
    conn = sqlite3.connect('server_control.db')
    cursor = conn.cursor()

    # Создайте таблицу "route", если она не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS route
                      (ip_route TEXT, ip_server TEXT, status INTEGER)''')

    # Отсканируйте ethernet порт и обработайте полученные данные
    # В примере просто добавляем фиктивную информацию о роутере
    router_ip = '192.168.1.1'
    server_ip = socket.gethostbyname(socket.gethostname())
    status = 1  # Предполагаем, что роутер доступен

    # Внесите информацию о роутере в базу данных
    cursor.execute("INSERT INTO route VALUES (?, ?, ?)", (router_ip, server_ip, status))
    conn.commit()

    # Закройте соединение с базой данных
    conn.close()

# Функция для обработки подключения клиентов
def handle_client_connection(client_socket):
    # Получите IP-адрес клиента
    client_ip = client_socket.getpeername()[0]

    # Создайте соединение с базой данных
    conn = sqlite3.connect('server_control.db')
    cursor = conn.cursor()

    # Получите информацию о ПК из базы данных по IP-адресу клиента
    cursor.execute("SELECT * FROM pc WHERE ip_pc = ?", (client_ip,))
    pc_data = cursor.fetchone()

    # Если информация о ПК найдена, обновите статус
    if pc_data:
        pc_id = pc_data[0]
        pc_status = 1  # Предполагаем, что ПК подключен
        cursor.execute("UPDATE pc SET status = ? WHERE id = ?", (pc_status, pc_id))
        conn.commit()

    # Закройте соединение с базой данных
    conn.close()

    # Закройте сокет клиента
    client_socket.close()

# Функция для ожидания подключений клиентов
def wait_for_clients():
    # Создайте сокет сервера
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Определите порт для прослушивания подключений
    port = 25678

    # Привяжите сокет сервера к заданному порту
    server_socket.bind(('0.0.0.0', port))

    # Прослушивайте подключения на сокете сервера
    server_socket.listen(5)

    while True:
        # Принимайте подключения от клиентов
        client_socket, address = server_socket.accept()

        # Обработайте подключение клиента в отдельном потоке или процессе
        handle_client_connection(client_socket)

# Вызовите функции для выполнения программы
scan_ethernet_port()
wait_for_clients()
