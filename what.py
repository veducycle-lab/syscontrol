import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTreeView, QTableView, QPlainTextEdit

class ZabbixInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Создаем панель навигации
        nav_tree = QTreeView(self)
        nav_tree.setGeometry(30, 30, 250, 500)

        # Создаем представление данных
        data_table = QTableView(self)
        data_table.setGeometry(290, 30, 670, 250)

        # Создаем таблицу с информацией
        info_table = QTableView(self)
        info_table.setGeometry(290, 320, 670, 250)

        # Создаем text area для вывода результатов
        result_text = QPlainTextEdit(self)
        result_text.setGeometry(30, 550, 930, 120)

        self.setGeometry(50, 50, 1000, 700)
        self.setWindowTitle('Zabbix-like Interface')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ZabbixInterface()
    sys.exit(app.exec_())
