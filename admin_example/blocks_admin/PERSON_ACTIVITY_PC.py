import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QTabWidget
from PyQt5.QtWidgets import QLabel, QVBoxLayout
import sqlite3


class PersonActivity(QWidget):
    def __init__(self):
        super().__init__()

        self.db_conn = sqlite3.connect('persons.db')
        self.db_cursor = self.db_conn.cursor()

        self.combo_box = QComboBox()
        self.tab_widget = QTabWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

        self.combo_box.currentIndexChanged.connect(self.update_tab_widget)

        self.populate_combo_box()

    def populate_combo_box(self):
        self.db_cursor.execute("SELECT DISTINCT day FROM current_session")
        days = self.db_cursor.fetchall()
        for day in days:
            self.combo_box.addItem(str(day[0]))
    
    def get_person_info(self, id_person):
        self.db_cursor.execute("SELECT name, second_name, third_name FROM person WHERE id_person = ?", (id_person,))
        person_info = self.db_cursor.fetchone()
        return person_info

    def update_tab_widget(self, index):
        selected_day = self.combo_box.currentText()
        self.tab_widget.clear()

        self.db_cursor.execute("SELECT id_current_session FROM current_session WHERE day = ?", (selected_day,))
        ids = self.db_cursor.fetchall()

        for id_current_session in ids:
            tab = QWidget()
            id_current_session_changed = id_current_session[0]
            self.db_cursor.execute("SELECT id_person FROM current_session WHERE id_current_session = ?", (id_current_session_changed,))
            idm = self.db_cursor.fetchall()
            idm_changed = idm[0][0]
            person_info = self.get_person_info(idm_changed)
            name = person_info[0]
            second_name = person_info[1]
            third_name = person_info[2]
            tab_name = f"{name} {second_name} {third_name}"
            self.tab_widget.addTab(tab, f"{tab_name}")

            layout = QVBoxLayout(tab)
            session_app_widget = self.create_session_app_widget(id_current_session[0])
            session_browse_widget = self.create_session_browse_widget(id_current_session[0])
            layout.addWidget(session_app_widget)
            layout.addWidget(session_browse_widget)

    def format_event_data(self, event_data):
        formatted_text = ""
        segments = event_data.strip("[]").split(" ")
        

        for segment in segments:
            text = segment.replace("(Пробел)", " (Пробел) ")
            texted = text.replace("(Enter)", "\n(Enter) ")
            for i in texted.split():
                if i == "(Пробел)":
                    formatted_text +=" "+ "<span style='background-color: yellow; border-radius: 10px; padding: 2px;'> (Пробел)</span> "
                elif i == "(Enter)":
                    formatted_text +="\n"+ "<span style='background-color: green; border-radius: 10px; padding: 2px;'> (Enter)</span> "
                else:
                    formatted_text += i

        return formatted_text

    def create_session_app_widget(self, id_current_session):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title_label = QLabel("Действия пользователя с приложениями\n")
        layout.addWidget(title_label)

        self.db_cursor.execute("SELECT name_process, window_size, id_event, event_data, time_start, time_end FROM session_stats_app WHERE id_current_session = ?", (id_current_session,))
        session_stats = self.db_cursor.fetchall()

        for stats in session_stats:
            name_process = QLabel(f"Название процесса: {stats[0]}")
            window_size = QLabel(f"Размер окна процесса: {stats[1]}")
            if 1 == stats[2]:
                id_event = QLabel(f"Наименование действия: Клик мышью")
            elif 2 == stats[2]:
                id_event = QLabel(f"Наименование действия: Ввод с клавиатуры")


            event_data = QLabel(f"Действия пользователя: {self.format_event_data(stats[3])}")
            if "-" in stats[5]:
                time_start = QLabel(f"Время когда произошло действие: {stats[4]}")
                razdel = QLabel("")
                layout.addWidget(name_process)
                layout.addWidget(window_size)
                layout.addWidget(id_event)
                layout.addWidget(event_data)
                layout.addWidget(time_start)
                layout.addWidget(razdel)
            else:
                time_start = QLabel(f"Время начала действий: {stats[4]}")
                time_end = QLabel(f"Время конца действий: {stats[5]}")
                razdel = QLabel("")
                layout.addWidget(name_process)
                layout.addWidget(window_size)
                layout.addWidget(id_event)
                layout.addWidget(event_data)
                layout.addWidget(time_start)
                layout.addWidget(time_end)
                layout.addWidget(razdel)  
            


        return widget

    def create_session_browse_widget(self, id_current_session):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title_label = QLabel("Действия пользователя в браузерах\n")
        layout.addWidget(title_label)

        self.db_cursor.execute("SELECT browse, window_size, tab, id_event, event_data, time_start, time_end FROM session_stats_browse WHERE id_current_session = ?", (id_current_session,))
        session_stats = self.db_cursor.fetchall()

        for stats in session_stats:
            browse = QLabel(f"Название браузера: {stats[0]}")
            window_size = QLabel(f"Размер окна процесса: {stats[1]}")
            tab = QLabel(f"Ссылка: {stats[2]}")

            if 1 == stats[3]:
                id_event = QLabel(f"Наименование действия: Клик мышью")
            elif 2 == stats[3]:
                id_event = QLabel(f"Наименование действия: Ввод с клавиатуры")


            event_data = QLabel(f"Действия пользователя: {self.format_event_data(stats[4])}")
            if "-" in stats[6]:
                time_start = QLabel(f"Время когда произошло действие: {stats[5]}")
                razdel = QLabel("")
                layout.addWidget(browse)
                layout.addWidget(window_size)
                layout.addWidget(tab)
                layout.addWidget(id_event)
                layout.addWidget(event_data)
                layout.addWidget(time_start)
                layout.addWidget(razdel)
            else:
                time_start = QLabel(f"Время начала действий: {stats[5]}")
                time_end = QLabel(f"Время конца действий: {stats[6]}")
                razdel = QLabel("")
                layout.addWidget(browse)
                layout.addWidget(window_size)
                layout.addWidget(tab)
                layout.addWidget(id_event)
                layout.addWidget(event_data)
                layout.addWidget(time_start)
                layout.addWidget(time_end)
                layout.addWidget(razdel)  

        return widget





if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = PersonActivity()
    widget.show()
    sys.exit(app.exec_())
