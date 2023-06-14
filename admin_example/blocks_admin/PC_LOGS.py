from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt

import sqlite3


class PClogs(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Server Control")
        self.layout = QVBoxLayout()
        self.resize(1901, 911)  # Установка размера окна

        # Создание QComboBox для выбора даты
        self.date_combo_box = QComboBox()
        self.date_combo_box.currentIndexChanged.connect(self.on_date_selected)
        self.layout.addWidget(self.date_combo_box)

        # Создание TabWidget для отображения данных по id_pc
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.load_dates_from_database()

        self.setLayout(self.layout)

    def load_dates_from_database(self):
        # Установка соединения с базой данных
        conn = sqlite3.connect('server_control.db')
        cursor = conn.cursor()

        # Выбор уникальных дат из колонки date в таблице pc_logs
        cursor.execute("SELECT DISTINCT substr(date, 1, 10) FROM pc_logs ORDER BY date")
        dates = cursor.fetchall()

        # Загрузка дат в QComboBox
        for date in dates:
            self.date_combo_box.addItem(date[0])

        conn.close()

    def load_pc_ids_by_date(self, selected_date):
        # Установка соединения с базой данных
        conn = sqlite3.connect('server_control.db')
        cursor = conn.cursor()

        # Выбор id_pc для выбранной даты
        cursor.execute("SELECT DISTINCT id_pc FROM pc_logs WHERE substr(date, 1, 10)=?", (selected_date,))
        pc_ids = cursor.fetchall()

        # Очистка предыдущих вкладок в TabWidget
        self.tab_widget.clear()

        # Создание новых вкладок в TabWidget
        for pc_id in pc_ids:
            tab = QWidget()
            tab_layout = QVBoxLayout()
            table = QTableWidget()

            # Установка заголовков колонок таблицы
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(['Время отправки', 'Кому отправлен', 'Тип протокола', 'Информация о протоколе'])

            # Получение данных из базы данных
            cursor.execute("SELECT substr(date, 12, 8), whom_sent, type_of_protocol, information_protocol FROM pc_logs WHERE id_pc=?", (pc_id[0],))
            logs = cursor.fetchall()

            # Установка количества строк в таблице
            table.setRowCount(len(logs))

            # Заполнение таблицы данными
            for row, log in enumerate(logs):
                for col in range(4):
                    item = QTableWidgetItem(str(log[col]))
                    table.setItem(row, col, item)

            # Растяжение колонки "Информация о протоколе" для полного отображения данных
            table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

            # Добавление таблицы в макет вкладки
            tab_layout.addWidget(table)
            tab.setLayout(tab_layout)

            # Добавление вкладки в TabWidget
            self.tab_widget.addTab(tab, f"ID PC: {pc_id[0]}")

        conn.close()

    def on_date_selected(self, index):
        selected_date = self.date_combo_box.itemText(index)
        self.load_pc_ids_by_date(selected_date)


if __name__ == '__main__':
    app = QApplication([])
    main_form = PClogs()
    main_form.show()
    app.exec_()
