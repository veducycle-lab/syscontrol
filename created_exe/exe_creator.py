import os
import shutil
import zipfile
import sqlite3
import subprocess
import socket
import netifaces
import wmi

# Получение основного шлюза Ethernet порта
def get_default_gateway():
    gateways = netifaces.gateways()
    if 'default' in gateways and netifaces.AF_INET in gateways['default']:
        return gateways['default'][netifaces.AF_INET][0]
    return None

# Получение MAC-адреса компьютера
def get_mac_address():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_LINK in addrs:
            mac_addr = addrs[netifaces.AF_LINK][0]['addr']
            if mac_addr != '00:00:00:00:00:00':
                return mac_addr
    return None

# Получение серийного номера загрузочного жесткого диска
def get_disk_serial_number():
    c = wmi.WMI()
    for physical_disk in c.Win32_DiskDrive():
        if physical_disk.DeviceID.startswith("\\\\.\\PHYSICALDRIVE0"):
            return physical_disk.SerialNumber.strip()

# Генерация ключей и запись их в базу данных
def generate_keys_and_save_to_db():
    # Получение необходимых данных
    gateway = get_default_gateway()
    mac_address = get_mac_address()
    disk_serial_number = get_disk_serial_number()

    # Формирование ключей
    admin_key = f"{gateway}/{mac_address}/{disk_serial_number}"
    client_key = f"{gateway}"

    # Создание/подключение к базе данных
    conn = sqlite3.connect('auth_keys.db')
    cursor = conn.cursor()

    # Создание таблицы sys_key, если она не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS sys_key
                      (auth_keys_client TEXT, auth_keys_admin TEXT)''')

    # Вставка ключей в таблицу
    cursor.execute('''INSERT INTO sys_key (auth_keys_client, auth_keys_admin)
                      VALUES (?, ?)''', (client_key, admin_key))

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

# Вызов функции для генерации ключей и записи их в базу данных
generate_keys_and_save_to_db()

# Получение текущего пути исполняемого файла
current_dir = os.path.dirname(os.path.abspath(__file__))

# Создание временной директории
temp_dir = os.path.join(current_dir, "temp")
os.makedirs(temp_dir, exist_ok=True)

# Копирование основного исполняемого скрипта
main_script = os.path.join(current_dir, "installer.py")
shutil.copy(main_script, temp_dir)

# Копирование архивов
archive1 = os.path.join(current_dir, "PortablePy.zip")
archive2 = os.path.join(current_dir, "admin_repo.zip")
archive3 = os.path.join(current_dir, "client_repo.zip")
shutil.copy(archive1, temp_dir)
shutil.copy(archive2, temp_dir)


# Копирование db-файла
db_file = os.path.join(current_dir, "auth_keys.db")
shutil.copy(db_file, temp_dir)

# Создание exe-файла с помощью PyInstaller
subprocess.call(['pyinstaller', '--onefile', '--add-data', f'{temp_dir};.', main_script])

# Удаление временной директории
shutil.rmtree(temp_dir)
