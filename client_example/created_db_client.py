import sqlite3
conn = sqlite3.connect('local_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE event (
        id_event INTEGER PRIMARY KEY,
        name TEXT
    )
''')

# Создание таблицы pc_recover в базе данных local_data.db
cursor.execute('''
    CREATE TABLE pc_recover (
        id_pc INTEGER,
        ip_pc TEXT,
        pc_name TEXT
    )
''')

# Создание таблицы server_recover в базе данных local_data.db
cursor.execute('''
    CREATE TABLE server_recover (
        ip_server TEXT
    )
''')
conn.commit()
conn.close()