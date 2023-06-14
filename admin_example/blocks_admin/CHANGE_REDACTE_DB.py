import os
import sqlite3
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout, QPushButton, QDialog, QLabel, QLineEdit, QMessageBox


class EditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Изменить запись")

        self.previous_data_label = QLabel("Предыдущая запись:")
        self.previous_data_lineedit = QLineEdit()
        self.previous_data_lineedit.setReadOnly(True)

        self.new_data_label = QLabel("Новая информация:")
        self.new_data_lineedit = QLineEdit()

        self.edit_button = QPushButton("Изменить")
        self.edit_button.clicked.connect(self.edit_data)

        layout = QVBoxLayout()
        layout.addWidget(self.previous_data_label)
        layout.addWidget(self.previous_data_lineedit)
        layout.addWidget(self.new_data_label)
        layout.addWidget(self.new_data_lineedit)
        layout.addWidget(self.edit_button)

        self.setLayout(layout)

    def setPreviousData(self, previous_data):
        self.previous_data_lineedit.setText(previous_data)

    def getNewData(self):
        return self.new_data_lineedit.text()

    def edit_data(self):
        new_data = self.getNewData()
        self.accept()


class DeleteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Удалить записи")

        self.message_label = QLabel("Желаете ли удалить выбранные строки?")

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_data)
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.cancel_delete)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout()
        layout.addWidget(self.message_label)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def delete_data(self):
        self.accept()

    def cancel_delete(self):
        self.reject()


class CreateDialog(QDialog):
    def __init__(self, column_names, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Создать запись")

        self.lineedits = []

        layout = QVBoxLayout()

        for column_name in column_names:
            label = QLabel(column_name)
            lineedit = QLineEdit()
            self.lineedits.append(lineedit)
            layout.addWidget(label)
            layout.addWidget(lineedit)

        create_button = QPushButton("Создать")
        create_button.clicked.connect(self.create_data)
        layout.addWidget(create_button)

        self.setLayout(layout)

    def create_data(self):
        data = []
        for lineedit in self.lineedits:
            data.append(lineedit.text())

        self.accept()


class SQLViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQL Viewer")
        self.resize(1901, 911)

        self.db_files = self.get_db_files()
        self.db_combobox = QComboBox()
        self.db_combobox.addItems(self.db_files)
        self.db_combobox.currentIndexChanged.connect(self.load_tables)

        self.table_combobox = QComboBox()
        self.table_combobox.currentIndexChanged.connect(self.load_table_data)

        self.table_widget = QTableWidget()

        self.edit_button = QPushButton("Изменить")
        self.edit_button.clicked.connect(self.show_edit_dialog)
        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.show_delete_dialog)
        self.create_button = QPushButton("Создать")
        self.create_button.clicked.connect(self.show_create_dialog)

        layout = QVBoxLayout()
        layout.addWidget(self.db_combobox)
        layout.addWidget(self.table_combobox)
        layout.addWidget(self.table_widget)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.create_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.connection = None
        self.enable_buttons()

    def enable_buttons(self):
        self.edit_button.setEnabled(True)
        self.delete_button.setEnabled(True)
        self.create_button.setEnabled(True)

    
    def get_db_files(self):
        db_files = []
        directory = os.path.expanduser("~/Desktop")
        for file in os.listdir(directory):
            if file.endswith(".db"):
                db_files.append(os.path.join(directory, file))
        return db_files

    def load_tables(self):
        db_file = self.db_combobox.currentText()
        self.table_combobox.clear()
        self.table_widget.clear()

        if self.connection:
            self.connection.close()

        self.connection = sqlite3.connect(db_file)
        cursor = self.connection.cursor()

        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        self.table_combobox.addItems([table[0] for table in tables])

        cursor.close()

    def load_table_data(self):
        table_name = self.table_combobox.currentText()

        if not table_name:
            return

        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name};")
        data = cursor.fetchall()

        column_names = [description[0] for description in cursor.description]
        self.table_widget.setColumnCount(len(column_names))
        self.table_widget.setRowCount(len(data))
        self.table_widget.setHorizontalHeaderLabels(column_names)

        for row_index, row_data in enumerate(data):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)  # Запретить редактирование
                self.table_widget.setItem(row_index, col_index, item)

        cursor.close()

    def show_edit_dialog(self):
        table_name = self.table_combobox.currentText()
        selected_item = self.table_widget.currentItem()
        if not table_name or not selected_item:
            return

        row_index = selected_item.row()
        column_index = selected_item.column()
        previous_data = selected_item.text()

        dialog = EditDialog(self)
        dialog.setPreviousData(previous_data)
        if dialog.exec_() == QDialog.Accepted:
            new_data = dialog.getNewData()
            item = QTableWidgetItem(new_data)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)  # Запретить редактирование
            self.table_widget.setItem(row_index, column_index, item)

            # Обновить значение в базе данных
            column_name = self.table_widget.horizontalHeaderItem(column_index).text()
            primary_key_column = self.table_widget.horizontalHeaderItem(0).text()  # Предполагается, что первая колонка - первичный ключ

            cursor = self.connection.cursor()
            cursor.execute(f"UPDATE {table_name} SET {column_name} = ? WHERE {primary_key_column} = ?",
                           (new_data, self.table_widget.item(row_index, 0).text()))
            self.connection.commit()
            cursor.close()

    def show_delete_dialog(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            return

        dialog = DeleteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            rows_to_delete = set()
            for item in selected_items:
                rows_to_delete.add(item.row())

            # Удалить строки из таблицы и базы данных
            table_name = self.table_combobox.currentText()
            primary_key_column = self.table_widget.horizontalHeaderItem(0).text()  # Предполагается, что первая колонка - первичный ключ

            cursor = self.connection.cursor()
            for row in sorted(rows_to_delete, reverse=True):
                primary_key_value = self.table_widget.item(row, 0).text()
                self.table_widget.removeRow(row)
                cursor.execute(f"DELETE FROM {table_name} WHERE {primary_key_column} = ?", (primary_key_value,))
            self.connection.commit()
            cursor.close()

    def show_create_dialog(self):
        table_name = self.table_combobox.currentText()
        if not table_name:
            return

        column_names = []
        for column_index in range(self.table_widget.columnCount()):
            column_names.append(self.table_widget.horizontalHeaderItem(column_index).text())

        dialog = CreateDialog(column_names, self)
        if dialog.exec_() == QDialog.Accepted:
            data = []
            for lineedit in dialog.lineedits:
                data.append(lineedit.text())

            # Добавить новую запись в таблицу и базу данных
            cursor = self.connection.cursor()
            cursor.execute(f"INSERT INTO {table_name} VALUES ({','.join(['?'] * len(data))})", data)
            self.connection.commit()
            cursor.close()

            # Обновить отображение таблицы
            self.load_table_data()


if __name__ == "__main__":
    app = QApplication([])
    window = SQLViewer()
    window.show()
    app.exec_()
