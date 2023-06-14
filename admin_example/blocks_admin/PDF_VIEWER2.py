import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QComboBox
from PyQt5.QtGui import QPixmap, QImage
import fitz
from openpyxl import load_workbook
import subprocess
import win32com.client as win32

class PDFWidget2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        pdf_path = 'PDF0_2.pdf'
        pdf_doc = fitz.open(pdf_path)
        pdf_page = pdf_doc.load_page(0)  # Получаем первую страницу

        # Создаем горизонтальный контейнер для размещения QComboBox и кнопки
        combobox_layout = QHBoxLayout()
        layout.addLayout(combobox_layout)

        # Создаем QComboBox
        combobox1 = QComboBox()
        combobox2 = QComboBox()

        # Получаем уникальные значения из колонки day таблицы current_session
        days = self.get_unique_days_from_database()
        
        # Добавляем уникальные значения в QComboBox
        combobox1.addItems(days)
        combobox2.addItems(days)

        # Добавляем QComboBox в горизонтальный контейнер
        combobox_layout.addWidget(combobox1)
        combobox_layout.addWidget(combobox2)

        generate_button = QPushButton("Сгенерировать")
        generate_button.clicked.connect(self.generate_pdf)
        layout.addWidget(generate_button)

        pixmap = QPixmap.fromImage(self.page_to_qimage(pdf_page))
        label = QLabel()
        label.setPixmap(pixmap)
        layout.addWidget(label)

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_pdf)
        layout.addWidget(save_button)

    def page_to_qimage(self, page):
        pix = page.get_pixmap()
        image = QImage(pix.samples, pix.width, pix.height, QImage.Format_RGB888)
        return image.copy()

    def save_pdf(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Сохранить PDF", "", "PDF Files (*.pdf)")

        if file_path:
            pdf_path = 'График работ.pdf'
            pdf_doc = fitz.open(pdf_path)
            pdf_page = pdf_doc.load_page(0)  # Получаем первую страницу

            pdf_writer = fitz.open()
            pdf_writer.insert_page(-1, width=pdf_page.width, height=pdf_page.height)
            pdf_writer[-1].show_pdf_page((0, 0, pdf_page.width, pdf_page.height), pdf_page)

            pdf_writer.save(file_path)

    def get_unique_days_from_database(self):
        connection = sqlite3.connect('persons.db')
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT day FROM current_session")
        days = cursor.fetchall()
        connection.close()

        return [str(day[0]) for day in days]

    def generate_data(self):
        combobox1 = self.findChild(QComboBox, "combobox1")
        combobox2 = self.findChild(QComboBox, "combobox2")

        selected_day1 = combobox1.currentText()
        selected_day2 = combobox2.currentText()

        print("Selected day 1:", selected_day1)
        print("Selected day 2:", selected_day2)

    def generate_pdf(self):
        input_file = 'PDF2.xlsx'
        output_file = 'PDF2.pdf'

        workbook = load_workbook(input_file)
        sheet = workbook['Sheet']

        combobox1 = self.findChild(QComboBox, "combobox1")
        combobox2 = self.findChild(QComboBox, "combobox2")

        selected_day1 = combobox1.currentText()
        selected_day2 = combobox2.currentText()

        # Загрузка данных в ячейки Excel
        sheet['S17'] = selected_day1
        sheet['T17'] = selected_day2

        connection = sqlite3.connect('persons.db')
        cursor = connection.cursor()

        # Получение id_current_session в промежутке выбранных дат
        cursor.execute("SELECT id_current_session FROM current_session WHERE day BETWEEN ? AND ?", (selected_day1, selected_day2))
        id_current_sessions = cursor.fetchall()

        # Получение данных из session_stats_browse по id_current_session
        data_rows = []
        for id_current_session in id_current_sessions:
            cursor.execute("SELECT * FROM session_stats_browse WHERE id_current_session=?", id_current_session)
            data_rows.extend(cursor.fetchall())

        connection.close()

        first_changer = 0
        second_changer = 0

        # Обработка данных из session_stats_browse
        for row in data_rows:
            tab = row[1]  # Замените 1 на соответствующий индекс столбца tab
            if tab in ['127.0.0.1', '192.168.0.1 - 192.168.3.255']:
                first_changer += 1
            else:
                second_changer += 1

        # Передача значений first_changer и second_changer в ячейки Excel
        sheet['S13'] = first_changer
        sheet['T13'] = second_changer

        # Сохранение изменений
        workbook.save(input_file)
        convert_excel_to_pdf(fr'C:\\Users\\user\\Desktop\\{input_file}', fr'C:\\Users\\user\\Desktop\\{output_file}')

def get_unique_hours(day1, day2):
    connection = sqlite3.connect('persons.db')
    cursor = connection.cursor()

    # Получение id_current_session для заданного диапазона дат
    cursor.execute("SELECT id_current_session FROM current_session WHERE day BETWEEN ? AND ?", (day1, day2))
    session_ids = cursor.fetchall()

    # Получение уникальных часов для полученных id_current_session
    unique_hours = set()
    for session_id in session_ids:
        cursor.execute("SELECT DISTINCT hours FROM current_session_hours WHERE id_current_session=?", (session_id[0],))
        hours = cursor.fetchall()
        unique_hours.update([hour[0] for hour in hours])

    connection.close()
    return unique_hours

def convert_excel_to_pdf(input_file, output_file):
    try:
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False
        workbook = excel.Workbooks.Open(input_file)
        workbook.ExportAsFixedFormat(0, output_file)
        workbook.Close()
        excel.Quit()
        print(f"Файл {input_file} успешно преобразован в PDF.")
    except Exception as e:
        print(f"Произошла ошибка при преобразовании в PDF: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = PDFWidget2()
    widget.show()
    sys.exit(app.exec_())
