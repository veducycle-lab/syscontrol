import sys
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QLabel, QHBoxLayout, QDialog, QSplitter, QTreeWidget, QTreeWidgetItem
from datetime import datetime

class ScrollAreaWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Создание Scroll Area и вертикального Layout
        scroll_area = QScrollArea(self)
        layout = QVBoxLayout()
        scroll_widget = QWidget()
        scroll_widget.setLayout(layout)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        # Подключение к базе данных persons.db
        conn = sqlite3.connect('persons.db')
        cursor = conn.cursor()

        # Получение данных из таблицы person
        cursor.execute("SELECT id_person, name, second_name, third_name FROM person")
        persons = cursor.fetchall()

        # Создание widget_scroll_area для каждого person и добавление их в Layout
        for person in persons:
            person_id = person[0]
            name = person[1]
            second_name = person[2]
            third_name = person[3]

            widget_scroll_area = QWidget()
            widget_scroll_area.setObjectName(f"person_{person_id}")
            widget_scroll_area.setStyleSheet("background-color: lightgray;")
            widget_scroll_area.setFixedHeight(50)
            widget_scroll_area.setContentsMargins(5, 5, 5, 5)
            widget_scroll_area.mousePressEvent = self.showPersonInfoWindow(person_id)

            label = QLabel(f"{name} {second_name} {third_name}", widget_scroll_area)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("background-color: transparent;")

            layout.addWidget(widget_scroll_area)
            widget_scroll_area.setLayout(QHBoxLayout())
            widget_scroll_area.layout().addWidget(label)

        # Закрытие соединения с базой данных
        conn.close()

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(scroll_area)

    def showPersonInfoWindow(self, person_id):
        def callback(event):
            global person_info_widget, profile_info_widget
            if person_info_widget:
                person_info_widget.close()
            if profile_info_widget:
                profile_info_widget.close()

            person_info_widget = PersonInfoWidget(person_id)
            profile_info_widget = ProfileInformationWidget(person_id)

            splitter.addWidget(person_info_widget)
            splitter.addWidget(profile_info_widget)

        return callback


class PersonInfoWidget(QWidget):
    def __init__(self, person_id):
        super().__init__()
        self.person_id = person_id
        
        self.initUI()

    def initUI(self):
        # Создание Scroll Area и вертикального Layout
        scroll_area = QScrollArea(self)
        layout = QVBoxLayout()
        scroll_widget = QWidget()
        scroll_widget.setLayout(layout)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        self.setFixedSize(250, 250)

        # Подключение к базе данных persons.db
        conn = sqlite3.connect('persons.db')
        cursor = conn.cursor()

        # Получение информации о person из таблицы person
        cursor.execute("SELECT * FROM person WHERE id_person = ?", (self.person_id,))
        person_info = cursor.fetchone()

        if person_info:
            person_widget = QWidget()
            person_layout = QVBoxLayout()
            person_widget.setLayout(person_layout)

            # Вывод информации о person
            name_label = QLabel(f"Name: {person_info[1]}", person_widget)
            second_name_label = QLabel(f"Second Name: {person_info[2]}", person_widget)
            third_name_label = QLabel(f"Third Name: {person_info[3]}", person_widget)

            person_layout.addWidget(name_label)
            person_layout.addWidget(second_name_label)
            person_layout.addWidget(third_name_label)

            layout.addWidget(person_widget)

        # Получение информации о доверии из таблицы person_trust
        cursor.execute("SELECT trust_factor FROM person_trust WHERE id_person = ?", (self.person_id,))
        trust_factor = cursor.fetchone()

        if trust_factor:
            trust_widget = QWidget()
            trust_layout = QVBoxLayout()
            trust_widget.setLayout(trust_layout)

            trust_label = QLabel("Доверие:", trust_widget)
            trust_label.setStyleSheet("font-weight: bold;")

            # Вывод графического элемента в зависимости от значения trust_factor
            if trust_factor[0] == 0:
                trust_text_label = QLabel("Не имеет доступа", trust_widget)
                trust_text_label.setStyleSheet("color: black;")
                trust_widget.setStyleSheet("background-color: gray;")
            elif trust_factor[0] == 1:
                trust_text_label = QLabel("Недоверие, возможно увольнение", trust_widget)
                trust_text_label.setStyleSheet("color: black;")
                trust_widget.setStyleSheet("background-color: red;")
            elif trust_factor[0] == 2:
                trust_text_label = QLabel("Неполное доверие", trust_widget)
                trust_text_label.setStyleSheet("color: black;")
                trust_widget.setStyleSheet("background-color: orange;")
            elif trust_factor[0] == 3:
                trust_text_label = QLabel("Полное доверие", trust_widget)
                trust_text_label.setStyleSheet("color: black;")
                trust_widget.setStyleSheet("background-color: green;")

            trust_layout.addWidget(trust_label)
            trust_layout.addWidget(trust_text_label)

            layout.addWidget(trust_widget)

        # Получение данных из таблицы person_app_network для данного person_id
        cursor.execute("SELECT * FROM person_app_network WHERE id_person = ? ORDER BY timestamp DESC",
                       (self.person_id,))
        app_network_data = cursor.fetchall()

        if app_network_data:
            app_network_widget = QWidget()
            app_network_layout = QVBoxLayout()
            app_network_widget.setLayout(app_network_layout)

            # Вывод данных из таблицы person_app_network
            for data in app_network_data:
                timestamp_label = QLabel(f"Timestamp: {data[1]}", app_network_widget)
                # Вывод остальных данных из таблицы person_app_network

                app_network_layout.addWidget(timestamp_label)
                # Добавьте код для вывода остальных данных

            layout.addWidget(app_network_widget)

        # Закрытие соединения с базой данных
        conn.close()

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(scroll_area)

    def getPersonName(self):
        conn = sqlite3.connect('persons.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM person WHERE id_person = ?", (self.person_id,))
        person_name = cursor.fetchone()[0]
        conn.close()
        return person_name
    
    # def showProfileInformation(self, item):
    #     if self.profile_info_widget:
    #         self.profile_info_widget.close()

    #     person_id = person_id.data(Qt.UserRole)
    #     self.profile_info_widget = ProfileInformationWidget(person_id)
    #     self.profile_info_widget.show()

class ProfileInformationWidget(QWidget):
    def __init__(self, person_id):
        super().__init__()
        self.person_id = person_id
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Информация о пользователе
        info_label = QLabel("Информация о пользователе:", self)
        info_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(info_label)

        # Получение имени пользователя
        person_name = self.getPersonName()

        # Получение информации о текущей сессии пользователя
        session_info = self.getSessionInfo()

        if session_info:
            pc_name = self.getPCName(session_info[0])
            pc_label = QLabel(f"Пользователь {person_name} сейчас использует {pc_name}", self)
            layout.addWidget(pc_label)

            active_devices = self.getActiveDevices()
            devices_label = QLabel("Активные устройства:", self)
            devices_label.setStyleSheet("font-weight: bold;")
            layout.addWidget(devices_label)

            if active_devices:
                devices_tree = QTreeWidget(self)
                devices_tree.setHeaderLabels(["Устройство"])
                for device in active_devices:
                    item = QTreeWidgetItem([device])
                    devices_tree.addTopLevelItem(item)
                layout.addWidget(devices_tree)
            else:
                no_devices_label = QLabel("Устройств не найдено", self)
                layout.addWidget(no_devices_label)

            app_info = self.getAppInfo(session_info[0])
            if app_info:
                app_label = QLabel("Сейчас использует программу:", self)
                app_label.setStyleSheet("font-weight: bold;")
                layout.addWidget(app_label)

                # Получение времени начала работы
                start_time = self.getStartTime(session_info[0])
                start_time_label = QLabel(f"Время начала работы: {start_time}", self)
                layout.addWidget(start_time_label)

                # Получение времени окончания работы
                end_time = self.getEndTime()
                end_time_label = QLabel(f"Время окончания: {end_time}", self)
                layout.addWidget(end_time_label)

                requests_count = self.getRequestsCount(session_info[1])
                requests_label = QLabel(f"Поступивших запросов: {requests_count}", self)
                layout.addWidget(requests_label)
            else:
                no_app_label = QLabel("Нет данных о текущей программе", self)
                layout.addWidget(no_app_label)
        else:
            no_session_label = QLabel("Пользователь не в сети", self)
            layout.addWidget(no_session_label)

        # Вывод информации о текущем времени и опоздании
        # current_time = datetime.now().strftime("%H:%M")
        # late_hours, late_minutes = self.calculateLateTime(current_time)
        # late_label = QLabel(f"Время начала работы: {start_time}", self)
        # layout.addWidget(late_label)

        self.setLayout(layout)

    def getPersonName(self):
        conn = sqlite3.connect('persons.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, second_name, third_name FROM person WHERE id_person = ?", (self.person_id,))
        person_data = cursor.fetchone()
        conn.close()
        if person_data:
            return f"{person_data[0]} {person_data[1]} {person_data[2]}"
        return ""

    def getSessionInfo(self):
        
        conn = sqlite3.connect('persons.db')
        cursor = conn.cursor()
        today = datetime.now().strftime("%d.%m.%Y")
        cursor.execute("SELECT id_pc, day FROM current_session WHERE id_person = ? AND day = ?", (self.person_id, today))
        session_info = cursor.fetchone()
        conn.close()
        return session_info

    def getPCName(self, pc_id):
        conn = sqlite3.connect('server_control.db')
        cursor = conn.cursor()
        cursor.execute("SELECT pc_name FROM pc WHERE id_pc = ?", (pc_id,))
        pc_name = cursor.fetchone()[0]
        conn.close()
        return pc_name

    def getActiveDevices(self):
        conn = sqlite3.connect('persons.db')
        cursor = conn.cursor()
        cursor.execute("SELECT device FROM person_devices WHERE id_person = ? AND date(timestamp) = date('now')", (self.person_id,))
        devices = cursor.fetchall()
        conn.close()
        return [device[0] for device in devices]

    def getAppInfo(self, pc_id):
        conn = sqlite3.connect('persons.db')
        cursor = conn.cursor()
        cursor.execute("SELECT time_start, time_end FROM session_stats_app WHERE id_current_session = ? ", (pc_id,))
        app_info = cursor.fetchone()
        conn.close()
        return app_info

    def getStartTime(self, pc_id):
        conn = sqlite3.connect('persons.db')
        cursor = conn.cursor()
        cursor.execute("SELECT MIN(hours), MIN(minutes) FROM current_session_hours WHERE id_current_session = ? GROUP BY hours", (pc_id,))
        start_time_info = cursor.fetchone()
        conn.close()
        if start_time_info:
            hours = start_time_info[0]
            minutes = start_time_info[1]
            return f"{hours}:{minutes}"
        return ""

    def getEndTime(self):
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M")
        if "08:30" <= current_time < "13:30" or "14:15" <= current_time < "19:30":
            return "Рабочий день еще не окончен"
        elif "19:30" <= current_time < "08:30":
            return "Рабочий день окончен"
        elif "13:30" <= current_time < "14:15":
            return "Обеденный перерыв"
        return ""

    def getRequestsCount(self, session_id):
        conn = sqlite3.connect('server_control.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM problems WHERE id_pc = ? AND id_person = ?", (session_id, self.person_id))
        requests_count = cursor.fetchone()[0]
        conn.close()
        return requests_count

    def calculateLateTime(self, current_time):
        start_time = "08:00"
        if current_time < start_time:
            start_time = "08:30"
            late_time = datetime.strptime(start_time, "%H:%M") - datetime.strptime(current_time, "%H:%M")
            late_hours = late_time.seconds // 3600
            late_minutes = (late_time.seconds // 60) % 60
            return late_hours, late_minutes
        elif current_time >= "08:30" and current_time < "13:30" or current_time >= "14:15" and current_time < "19:30":
            return 0, 0
        else:
            start_time = "08:30"
            late_time = datetime.strptime(current_time, "%H:%M") - datetime.strptime(start_time, "%H:%M")
            late_hours = late_time.seconds // 3600
            late_minutes = (late_time.seconds // 60) % 60
            return late_hours, late_minutes

    def addLateTimeLabel(self, layout):
        current_time = datetime.now().strftime("%H:%M")
        late_hours, late_minutes = self.calculateLateTime(current_time)
        if late_hours > 0 or late_minutes > 0:
            late_label = QLabel(f"Работник опоздал на {late_hours} часов {late_minutes} минут", self)
        else:
            late_label = QLabel("Работник не опоздал", self)
        layout.addWidget(late_label)

    def addScreenshotsTree(self, layout):
        screenshots = self.getScreenshots()
        if screenshots:
            screenshots_tree = QTreeWidget(self)
            screenshots_tree.setHeaderLabels(["Снимок экрана"])
            for screenshot in screenshots:
                item = QTreeWidgetItem([screenshot])
                screenshots_tree.addTopLevelItem(item)
            layout.addWidget(screenshots_tree)
        else:
            no_screenshots_label = QLabel("Скриншотов не найдено", self)
            layout.addWidget(no_screenshots_label)

    def getScreenshots(self):
        conn = sqlite3.connect('persons.db')
        cursor = conn.cursor()
        cursor.execute("SELECT screen_info FROM person_screen WHERE id_person = ?", (self.person_id,))
        screenshots = cursor.fetchall()
        conn.close()
        return [screenshot[0] for screenshot in screenshots]

    def updateUI(self):
        layout = QVBoxLayout()

        info_label = QLabel("Информация о пользователе:", self)
        info_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(info_label)

        person_name = self.getPersonName()
        session_info = self.getSessionInfo()

        if session_info:
            pc_name = self.getPCName(session_info[0])
            pc_label = QLabel(f"Пользователь {person_name} сейчас использует {pc_name}", self)
            layout.addWidget(pc_label)

            active_devices = self.getActiveDevices()
            devices_label = QLabel("Активные устройства:", self)
            devices_label.setStyleSheet("font-weight: bold;")
            layout.addWidget(devices_label)

            if active_devices:
                devices_tree = QTreeWidget(self)
                devices_tree.setHeaderLabels(["Устройство"])
                for device in active_devices:
                    item = QTreeWidgetItem([device])
                    devices_tree.addTopLevelItem(item)
                layout.addWidget(devices_tree)
            else:
                no_devices_label = QLabel("Устройств не найдено", self)
                layout.addWidget(no_devices_label)

            app_info = self.getAppInfo(session_info[0])
            if app_info:
                app_label = QLabel("Сейчас использует программу:", self)
                app_label.setStyleSheet("font-weight: bold;")
                layout.addWidget(app_label)

                start_time = self.getStartTime(session_info[0])
                start_time_label = QLabel(f"Время начала работы: {start_time}", self)
                layout.addWidget(start_time_label)

                end_time = self.getEndTime()
                end_time_label = QLabel(f"Время окончания: {end_time}", self)
                layout.addWidget(end_time_label)

                requests_count = self.getRequestsCount(session_info[1])
                requests_label = QLabel(f"Поступивших запросов: {requests_count}", self)
                layout.addWidget(requests_label)

                self.addLateTimeLabel(layout)
                self.addScreenshotsTree(layout)
            else:
                no_app_label = QLabel("Нет данных о текущей программе", self)
                layout.addWidget(no_app_label)
        else:
            no_session_label = QLabel("Пользователь не в сети", self)
            layout.addWidget(no_session_label)

        self.setLayout(layout)

    def updateData(self, person_id):
        self.person_id = person_id
        self.updateUI()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    splitter = QSplitter(Qt.Horizontal)
    scroll_area_widget = ScrollAreaWidget()
    splitter.addWidget(scroll_area_widget)
    splitter.setSizes([200, 200])

    person_info_widget = None
    profile_info_widget = None

    splitter.show()
    sys.exit(app.exec_())
