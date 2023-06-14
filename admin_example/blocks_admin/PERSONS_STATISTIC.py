import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QDialog, QAbstractScrollArea, QGridLayout, QMainWindow
from PyQt5.QtGui import QColor
import sqlite3


class Dialog(QDialog):
    def __init__(self, column, login, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Вы просматриваете {column} час, пользователя {login}")

        layout = QGridLayout()
        self.setLayout(layout)

        # Создание пустой таблицы
        table = QTableWidget()
        table.setRowCount(0)
        table.setColumnCount(60)  # Количество колонок
        headers = [f"{i:02d}" for i in range(60)]  # Заголовки колонок от 00 до 59
        table.setHorizontalHeaderLabels(headers)
        layout.addWidget(table)


class PersonStatistic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Подключение к базе данных
        conn = sqlite3.connect('persons.db')
        self.cursor = conn.cursor()

        # Получение уникальных значений из колонки "day"
        self.cursor.execute("SELECT DISTINCT day FROM current_session ORDER BY day")
        self.days = self.cursor.fetchall()

        # Создание виджета таблицы
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Создание таблиц для каждого уникального значения "day"
        for day in self.days:
            # Создание таблицы
            table = QTableWidget()
            layout.addWidget(table)

            # Запрос данных для текущего значения "day" из таблицы current_session
            self.cursor.execute("SELECT id_current_session FROM current_session WHERE day = ? ORDER BY id_current_session",
                                day)
            ids = self.cursor.fetchall()

            # Создание списка уникальных id_current_session
            unique_ids = list(set(ids))

            # Установка числа строк в таблице
            table.setRowCount(len(unique_ids))
            table.setColumnCount(27)  # Количество колонок

            # Установка размеров колонок
            headers = ['Пользователь', '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13',
                       '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', 'Начало', 'Окончание']
            table.setHorizontalHeaderLabels(headers)

            # Установка размеров колонок
            for col, header in enumerate(headers):
                if header in ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13',
                              '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']:
                    table.setColumnWidth(col, len(header) * 10)

            # Установка политики размеров таблицы
            table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

            # Заполнение таблицы данными
            for row, id_current_session in enumerate(unique_ids):
                # Получение данных о пользователе по id_current_session из таблицы current_session
                id_current_session = id_current_session[0]  # Преобразование кортежа в значение
                self.cursor.execute("SELECT id_person FROM current_session WHERE id_current_session = ?", (id_current_session,))
                id_person = self.cursor.fetchone()[0]
                self.cursor.execute("SELECT login FROM person_login_psswd WHERE id_person = ?", (id_person,))
                login = self.cursor.fetchone()[0]

                # Установка значения в столбце "Пользователь"
                item = QTableWidgetItem(login)
                table.setItem(row, 0, item)

                # Получение значений hours для текущего id_current_session
                self.cursor.execute("SELECT hours FROM current_session_hours WHERE id_current_session = ? ORDER BY hours", (id_current_session,))
                hours = self.cursor.fetchall()

                # Проверка и установка цвета для колонок '20', '21', '22', '23'
                orange_cols = ['20', '21', '22', '23']
                orange_hours = [h[0] for h in hours if h[0] in orange_cols]
                gray_cols = [col for col in orange_cols if col not in orange_hours]

            # Заполнение таблицы данными
            for row, id_current_session in enumerate(unique_ids):
                # Получение данных о пользователе по id_current_session из таблицы current_session
                id_current_session = id_current_session[0]  # Преобразование кортежа в значение
                self.cursor.execute("SELECT id_person FROM current_session WHERE id_current_session = ?", (id_current_session,))
                id_person = self.cursor.fetchone()[0]
                self.cursor.execute("SELECT login FROM person_login_psswd WHERE id_person = ?", (id_person,))
                login = self.cursor.fetchone()[0]

                # Установка значения в столбце "Пользователь"
                item = QTableWidgetItem(login)
                table.setItem(row, 0, item)

                # Получение значений hours для текущего id_current_session
                self.cursor.execute("SELECT hours FROM current_session_hours WHERE id_current_session = ? ORDER BY hours", (id_current_session,))
                hours = self.cursor.fetchall()

                # Установка цвета для колонок '00', '01', '02', '03', '04', '05', '06', '07'
                for col, header in enumerate(headers[1:9], start=1):
                    if header in [h[0] for h in hours]:
                        item = QTableWidgetItem('')
                        item.setBackground(QColor('green'))
                        table.setItem(row, col, item)
                    else:
                        item = QTableWidgetItem('')
                        item.setBackground(QColor(192, 192, 192))  # Серый цвет
                        table.setItem(row, col, item)

                # Проверка и установка цвета для колонок '20', '21', '22', '23'
                orange_cols = ['20', '21', '22', '23']
                orange_hours = [h[0] for h in hours if h[0] in orange_cols]
                gray_cols = [col for col in orange_cols if col not in orange_hours]

                for col, header in enumerate(headers[9:25], start=9):
                    if header in [h[0] for h in hours]:
                        item = QTableWidgetItem('')
                        item.setBackground(QColor('green'))
                        table.setItem(row, col, item)
                    elif header in gray_cols:
                        item = QTableWidgetItem('')
                        item.setBackground(QColor(192, 192, 192))  # Серый цвет
                        table.setItem(row, col, item)
                    else:
                        item = QTableWidgetItem('')
                        item.setBackground(QColor('red'))
                        table.setItem(row, col, item)

                # Установка цвета для колонок '20', '21', '22', '23'
                for col, header in enumerate(orange_cols, start=21):
                    item = QTableWidgetItem('')
                    if header in orange_hours:
                        item.setBackground(QColor('orange'))
                    else:
                        item.setBackground(QColor(192, 192, 192))  # Серый цвет
                    table.setItem(row, col, item)      

                    
            for row, id_current_session in enumerate(unique_ids):
                # Получение данных о пользователе по id_current_session из таблицы current_session
                id_current_session = id_current_session[0]  # Преобразование кортежа в значение
                self.cursor.execute("SELECT id_person FROM current_session WHERE id_current_session = ?", (id_current_session,))
                id_person = self.cursor.fetchone()[0]
                self.cursor.execute("SELECT login FROM person_login_psswd WHERE id_person = ?", (id_person,))
                login = self.cursor.fetchone()[0]

                # Установка значения в столбце "Пользователь"
                item = QTableWidgetItem(login)
                table.setItem(row, 0, item)

                # Получение значений hours и minutes для текущего id_current_session
                self.cursor.execute("SELECT hours, minutes FROM current_session_hours WHERE id_current_session = ? ORDER BY hours, minutes", (id_current_session,))
                hours_minutes = self.cursor.fetchall()

                # Создание списка уникальных значений hours
                unique_hours = list(set([hm[0] for hm in hours_minutes]))

                # Заполнение значений для колонки "Начало"
                if hours_minutes:
                    min_start_hour = min(unique_hours)
                    min_start_minutes = min([hm[1] for hm in hours_minutes if hm[0] == min_start_hour])
                    start_time = f"{min_start_hour}:{min_start_minutes:02}"
                    table.setItem(row, 25, QTableWidgetItem(start_time))

                # Заполнение значений для колонки "Окончание"
                if hours_minutes:
                    max_end_hour = max(unique_hours)
                    max_end_minutes = max([hm[1] for hm in hours_minutes if hm[0] == max_end_hour])
                    end_time = f"{max_end_hour}:{max_end_minutes:02}"
                    table.setItem(row, 26, QTableWidgetItem(end_time))


    def open_dialog(self, item):
        # Получение значения колонки и логина выбранной строки
        table = self.sender()
        column_header = table.horizontalHeaderItem(item.column()).text()
        login_item = table.item(item.row(), 0)
        login = login_item.text()

        # Открытие диалогового окна
        dialog = Dialog(column_header, login)
        dialog.exec_()



if __name__ == '__main__':
    # Создание приложения
    app = QApplication(sys.argv)

    # Создание главного окна
    window = QMainWindow()
    widget = PersonStatistic(window)
    window.setCentralWidget(widget)
    window.show()

    # Запуск главного цикла приложения
    sys.exit(app.exec_())