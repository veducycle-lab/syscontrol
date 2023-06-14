import os
import psutil
import sqlite3
import psycopg2
import pyodbc
import mysql.connector
import cx_Oracle


def check_database_connection(db_type, host, port, username, password):
    try:
        if db_type == 'PostgreSQL':
            conn = psycopg2.connect(host=host, port=port, user=username, password=password)
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            cursor.close()
            conn.close()
            return True

        elif db_type == 'Microsoft SQL':
            conn = pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={host},{port};DATABASE=master;UID={username};PWD={password}'
            )
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            cursor.close()
            conn.close()
            return True

        elif db_type == 'MySQL':
            conn = mysql.connector.connect(host=host, port=port, user=username, password=password)
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            cursor.close()
            conn.close()
            return True

        elif db_type == 'Oracle':
            dsn = cx_Oracle.makedsn(host, port, service_name='SERVICE_NAME')
            conn = cx_Oracle.connect(username, password, dsn=dsn)
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM DUAL')
            cursor.close()
            conn.close()
            return True

    except Exception as e:
        # В случае возникновения ошибки при подключении, можно вывести сообщение или логировать ошибку
        print(f'Ошибка подключения к базе данных {db_type}: {e}')

    return False


def find_databases():
    databases = []

    # Поиск баз данных в папках
    database_folders = [
        {'name': 'PostgreSQL', 'path': '/path/to/postgresql/folder'},
        {'name': 'Microsoft SQL', 'path': '/path/to/mssql/folder'},
        {'name': 'MySQL', 'path': '/path/to/mysql/folder'},
        {'name': 'Oracle', 'path': '/path/to/oracle/folder'}
    ]

    for db_folder in database_folders:
        if os.path.exists(db_folder['path']):
            databases.append(db_folder['name'])

    # Поиск запущенных баз данных в процессах
    running_processes = psutil.process_iter(['pid', 'name'])

    for process in running_processes:
        process_name = process.info['name'].lower()

        if 'postgresql' in process_name:
            databases.append('PostgreSQL')
        elif 'sqlservr' in process_name:
            databases.append('Microsoft SQL')
        elif 'mysqld' in process_name:
            databases.append('MySQL')
        elif 'oracle' in process_name:
            databases.append('Oracle')

    return databases


def save_database_info(database_name, status, login=None, password=None):
    conn = sqlite3.connect('server_control.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO existing_db (name_db, status, login, password) VALUES (?, ?, ?, ?)",
                   (database_name, status, login, password))

    conn.commit()
    conn.close()


if __name__ == '__main__':
    databases = find_databases()

    if 'PostgreSQL' in databases:
        print('Найдена база данных PostgreSQL')
        # Здесь можно запросить порт, логин и пароль с помощью диалогового окна в cmd
        port = input('Введите порт для подключения к PostgreSQL: ')
        login = input('Введите логин для подключения к PostgreSQL: ')
        password = input('Введите пароль для подключения к PostgreSQL: ')

        if check_database_connection('PostgreSQL', 'localhost', port, login, password):
            save_database_info('PostgreSQL', 1, login, password)
            print('Успешно сохранена информация о базе данных PostgreSQL')
        else:
            save_database_info('PostgreSQL', 0)
            print('Не удалось подключиться к базе данных PostgreSQL')

    if 'Microsoft SQL' in databases:
        print('Найдена база данных Microsoft SQL')
        # Здесь можно запросить порт, логин и пароль с помощью диалогового окна в cmd
        port = input('Введите порт для подключения к Microsoft SQL: ')
        login = input('Введите логин для подключения к Microsoft SQL: ')
        password = input('Введите пароль для подключения к Microsoft SQL: ')

        if check_database_connection('Microsoft SQL', 'localhost', port, login, password):
            save_database_info('Microsoft SQL', 1, login, password)
            print('Успешно сохранена информация о базе данных Microsoft SQL')
        else:
            save_database_info('Microsoft SQL', 0)
            print('Не удалось подключиться к базе данных Microsoft SQL')

    if 'MySQL' in databases:
        print('Найдена база данных MySQL')
        # Здесь можно запросить порт, логин и пароль с помощью диалогового окна в cmd
        port = input('Введите порт для подключения к MySQL: ')
        login = input('Введите логин для подключения к MySQL: ')
        password = input('Введите пароль для подключения к MySQL: ')

        if check_database_connection('MySQL', 'localhost', port, login, password):
            save_database_info('MySQL', 1, login, password)
            print('Успешно сохранена информация о базе данных MySQL')
        else:
            save_database_info('MySQL', 0)
            print('Не удалось подключиться к базе данных MySQL')

    if 'Oracle' in databases:
        print('Найдена база данных Oracle')
        # Здесь можно запросить порт, логин и пароль с помощью диалогового окна в cmd
        port = input('Введите порт для подключения к Oracle: ')
        login = input('Введите логин для подключения к Oracle: ')
        password = input('Введите пароль для подключения к Oracle: ')

        if check_database_connection('Oracle', 'localhost', port, login, password):
            save_database_info('Oracle', 1, login, password)
            print('Успешно сохранена информация о базе данных Oracle')
        else:
            save_database_info('Oracle', 0)
            print('Не удалось подключиться к базе данных Oracle')
