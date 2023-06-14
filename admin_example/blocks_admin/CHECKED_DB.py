import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont

class DBController(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DB Controller')
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        # Виджет 1: Статус внутренней базы данных
        widget_db_internal = self.create_db_widget('LocalStorage', 'icon_db.png')
        layout.addWidget(widget_db_internal)
        
        # Виджет 2: Статус базы данных PostgreSQL
        widget_db_postgres = self.create_db_widget('PostgreSQL', 'postgressql.png')
        layout.addWidget(widget_db_postgres)
        
        # Виджет 3: Статус базы данных Microsoft SQL
        widget_db_mssql = self.create_db_widget('Microsoft SQL', 'microsoftsql.png')
        layout.addWidget(widget_db_mssql)
        
        # Виджет 4: Статус базы данных MySQL
        widget_db_mysql = self.create_db_widget('MySQL', 'mysql.png')
        layout.addWidget(widget_db_mysql)
        
        # Виджет 5: Статус базы данных Oracle
        widget_db_oracle = self.create_db_widget('Oracle', 'oracle.png')
        layout.addWidget(widget_db_oracle)
        
        self.setLayout(layout)
    
    def create_db_widget(self, db_name, icon_path):
        widget = QWidget()
        
        layout = QHBoxLayout()
        
        label_image = QLabel()
        pixmap = QPixmap(icon_path)
        label_image.setPixmap(pixmap.scaledToWidth(200))
        layout.addWidget(label_image)
        
        label_text = QLabel(self.get_db_status(db_name))
        label_text.setFont(QFont('Arial', 12))
        layout.addWidget(label_text)
        
        widget.setLayout(layout)
        
        return widget
    
    def get_db_status(self, db_name):
        status_text = f'Статус базы данных {db_name}:'
        image_path = 'gray.png'  # Используем серую иконку для неустановленной базы данных
        
        # Соединяемся с базой данных server_control.db
        conn = sqlite3.connect('server_control.db')
        cursor = conn.cursor()
        
        # Ищем запись в таблице existing_db с указанным db_name
        cursor.execute("SELECT status FROM existing_db WHERE name_db=?", (db_name,))
        row = cursor.fetchone()
        if row is not None:
            status = row[0]
            if status == 1:
                status_text += ' БД доступна для взаимодействия'
                image_path = 'green.png'  # Используем зеленую иконку для статуса "Онлайн"
            else:
                status_text += ' БД недоступна для взаимодействия'
                image_path = 'red.png'  # Используем красную иконку для статуса "Офлайн"
        else:
            status_text += ' БД не найдена на устройстве'
        conn.close()
        
        # Добавляем иконку справа от текста статуса
        status_text += f" <img src='{image_path}' width='15' height='15'>"
        
        return status_text


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = DBController()
    controller.show()
    sys.exit(app.exec_())
