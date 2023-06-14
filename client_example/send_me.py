import sqlite3
import socket
import psutil
import time

conn = sqlite3.connect('local_data.db')
cursor = conn.cursor()
cursor.execute('SELECT ip_server FROM server_recover')
ip_server = cursor.fetchone()[0]
conn.close()

def get_next_pc_name():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for port in range(25678, 25979):
        try:
            client_socket.connect((ip_server, port))
            client_socket.send("GET_NEXT_PC_NAME".encode())
            response = client_socket.recv(1024).decode()
            client_socket.close()
            return response
        except ConnectionRefusedError:
            continue
    client_socket.close()
    return None

ip_pc = socket.gethostbyname(socket.gethostname())
mac = ':'.join(['{:02x}'.format((int(i, 16))) for i in psutil.net_if_addrs()['Ethernet'][0].address.split(':')])
serial_number = psutil.win32_products()[0].serial
os_version = psutil.win32_edition_info().current_version
pc_name = get_next_pc_name()

if pc_name:
    server_conn = sqlite3.connect('server_control.db')
    server_cursor = server_conn.cursor()
    server_cursor.execute("INSERT INTO pc (ip_pc, pc_name, MAC, PC_serial_number, OC) VALUES (?, ?, ?, ?, ?)",
                          (ip_pc, pc_name, mac, serial_number, os_version))
    server_conn.commit()
    server_conn.close()


server_port = None
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
for port in range(25678, 25979):
    try:
        client_socket.connect((ip_server, port))
        server_port = port
        break
    except ConnectionRefusedError:
        continue

if server_port:
    data = f"{ip_pc},{pc_name},{mac},{serial_number},{os_version}"
    client_socket.send(data.encode())

    while True:
        time.sleep(0.005)
        client_socket.send("KEEP_ALIVE".encode())


client_socket.close()
