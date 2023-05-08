import sqlite3

# Создание подключения к базе данных
conn = sqlite3.connect('syscontrol.db')


conn.close()