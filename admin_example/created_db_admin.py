import sqlite3

server_conn = sqlite3.connect('server_control.db')
server_cursor = server_conn.cursor()

server_cursor.execute('''CREATE TABLE pc (
    id_pc INTEGER PRIMARY KEY,
    ip_pc TEXT,
    pc_name TEXT,
    MAC TEXT,
    PC_serial_number TEXT,
    OC TEXT,
    connection_type TEXT CHECK (connection_type IN ('LAN', 'Wireless')),
    status INTEGER CHECK (status = 0 OR status = 1),
    id_route INTEGER,
    ip_route TEXT,
    FOREIGN KEY (id_route) REFERENCES route(id_route),
    FOREIGN KEY (ip_route) REFERENCES route(ip_route)
)''')

server_cursor.execute('''
    CREATE TABLE pc_activity (
        id_pc_activity INTEGER PRIMARY KEY,
        id_pc INTEGER,
        network_data TEXT,
        timestamp DATETIME,
        FOREIGN KEY (id_pc) REFERENCES pc (id_pc)
    )
''')

server_cursor.execute('''
    CREATE TABLE route_activity (
        id_route_activity INTEGER PRIMARY KEY,
        id_pc INTEGER,
        id_route INTEGER,
        network_data TEXT,
        timestamp DATETIME,
        FOREIGN KEY (id_pc) REFERENCES pc (id_pc),
        FOREIGN KEY (id_route) REFERENCES route (id_route)
    )
''')

server_cursor.execute('''
    CREATE TABLE existing_db (
        id_exist_db INTEGER PRIMARY KEY,
        name_db TEXT,
        port INTEGER,
        login TEXT,
        password TEXT,
        status INTEGER
    )
''')

server_cursor.execute('''CREATE TABLE server (
    id_server INTEGER PRIMARY KEY,
    ip_server TEXT,
    server_name TEXT,
    submask TEXT,
    ip_internet TEXT
)''')

server_cursor.execute('''CREATE TABLE route (
    id_route INTEGER PRIMARY KEY,
    ip_route TEXT,
    route_name TEXT,
    ip_server TEXT,
    status INTEGER CHECK (status = 0 OR status = 1),
    FOREIGN KEY (ip_server) REFERENCES server(ip_server)
)''')

server_conn.execute('''
    CREATE TABLE problems (
        id_problem INTEGER PRIMARY KEY,
        problem TEXT,
        id_pc INTEGER,
        id_person INTEGER,
        FOREIGN KEY (id_pc) REFERENCES pc(id_pc),
        FOREIGN KEY (id_person) REFERENCES person(id_person)
    )
''')

server_conn.execute('''
    CREATE TABLE pc_logs (
        id_pc INTEGER,
        date DATETIME,
        whom_sent TEXT,
        type_of_protocol TEXT,
        information_protocol TEXT,
        FOREIGN KEY (id_pc) REFERENCES pc (id_pc)
    )
''')

server_conn.commit()
server_conn.close()



persons_conn = sqlite3.connect('persons.db')
persons_cursor = persons_conn.cursor()

persons_cursor.execute('''CREATE TABLE person (
    id_person INTEGER PRIMARY KEY,
    name TEXT,
    second_name TEXT,
    third_name TEXT,
    phone_number TEXT,
    email TEXT,
    field_of_activity TEXT,
    employment_date TEXT,
    dismissal_date TEXT
)''')

persons_cursor.execute('''CREATE TABLE person_trust (
    id_person INTEGER,
    trust_factor INTEGER,
    FOREIGN KEY (id_person) REFERENCES person(id_person)
)''')

persons_cursor.execute('''CREATE TABLE person_login_psswd (
    id_login INTEGER PRIMARY KEY,
    login TEXT,
    psswd TEXT,
    id_person INTEGER,
    FOREIGN KEY (id_person) REFERENCES person(id_person)
)''')

persons_cursor.execute('''
    CREATE TABLE IF NOT EXISTS person_statistic_start (
        id_pc INTEGER,
        id_person INTEGER,
        time_start DATE,
        day DATE,
        FOREIGN KEY (id_pc) REFERENCES server_control.pc(id_pc),
        FOREIGN KEY (id_person) REFERENCES person(id_person)
    )
''')

persons_cursor.execute('''
    CREATE TABLE IF NOT EXISTS person_statistic_end (
        id_pc INTEGER,
        id_person INTEGER,
        time_end DATE,
        day DATE,
        FOREIGN KEY (id_pc) REFERENCES server_control.pc(id_pc),
        FOREIGN KEY (id_person) REFERENCES person(id_person)
    )
''')

persons_cursor.execute('''CREATE TABLE person_activity (
    id_p_activity INTEGER PRIMARY KEY,
    id_person INTEGER,
    id_pc INTEGER,
    clicked_app TEXT,
    timestamp TEXT,
    FOREIGN KEY (id_person) REFERENCES person(id_person),
    FOREIGN KEY (id_pc) REFERENCES pc(id_pc)
)''')

persons_cursor.execute('''CREATE TABLE person_browse_activity (
    id_pb_activity INTEGER PRIMARY KEY,
    id_p_activity INTEGER,
    browse TEXT,
    tab TEXT,
    element TEXT,
    keyboard_activity TEXT,
    mouse_activity TEXT,
    FOREIGN KEY (id_p_activity) REFERENCES person_activity(id_p_activity)
)''')

persons_cursor.execute('''CREATE TABLE person_app_activity (
    id_ab_activity INTEGER PRIMARY KEY,
    id_p_activity INTEGER,
    keyboard_activity TEXT,
    mouse_activity TEXT,
    FOREIGN KEY (id_p_activity) REFERENCES person_activity(id_p_activity)
)''')

persons_cursor.execute('''CREATE TABLE person_app_network (
    id_ap INTEGER PRIMARY KEY,
    id_person INTEGER,
    id_pc INTEGER,
    app TEXT,
    network_data TEXT,
    timestamp TEXT,
    FOREIGN KEY (id_person) REFERENCES person(id_person),
    FOREIGN KEY (id_pc) REFERENCES pc(id_pc)
)''')

persons_cursor.execute('''CREATE TABLE person_devices (
    id_p_devices INTEGER PRIMARY KEY,
    id_person INTEGER,
    id_pc INTEGER,
    device TEXT,
    timestamp TEXT,
    FOREIGN KEY (id_person) REFERENCES person(id_person),
    FOREIGN KEY (id_pc) REFERENCES pc(id_pc)
)''')

persons_cursor.execute('''CREATE TABLE person_devices_activity (
    id_pd_activity INTEGER PRIMARY KEY,
    id_p_devices INTEGER,
    file_activity TEXT,
    timestamp TEXT,
    FOREIGN KEY (id_p_devices) REFERENCES person_devices(id_p_devices)
)''')

persons_cursor.execute('''CREATE TABLE person_screen (
    id_p_screen INTEGER PRIMARY KEY,
    id_person INTEGER,
    id_pc INTEGER,
    screen_info TEXT,
    timestamp TEXT,
    FOREIGN KEY (id_person) REFERENCES person(id_person),
    FOREIGN KEY (id_pc) REFERENCES pc(id_pc)
)''')

persons_cursor.execute('''
    CREATE TABLE event (
        id_event INTEGER PRIMARY KEY,
        name TEXT
    )
''')

persons_cursor.execute('''
    CREATE TABLE current_session (
        id_current_session INTEGER PRIMARY KEY,
        id_pc INTEGER,
        id_person INTEGER,
        day DATETIME,
        FOREIGN KEY (id_pc) REFERENCES pc (id_pc),
        FOREIGN KEY (id_person) REFERENCES person (id_person)
    )
''')

persons_cursor.execute('''
    CREATE TABLE session_stats_app (
        id_session_stats_app INTEGER PRIMARY KEY,
        id_current_session INTEGER,
        name_process TEXT,
        window_size TEXT,
        id_event INTEGER,
        event_data TEXT,
        time_start DATETIME,
        time_end DATETIME,
        FOREIGN KEY (id_current_session) REFERENCES current_session (id_current_session),
        FOREIGN KEY (id_event) REFERENCES event (id_event)
    )
''')

persons_cursor.execute('''
    CREATE TABLE session_stats_browse (
        id_session_stats_browse INTEGER PRIMARY KEY,
        id_current_session INTEGER,
        browse TEXT,
        window_size TEXT,
        tab TEXT,
        id_event INTEGER,
        event_data TEXT,
        time_start DATETIME,
        time_end DATETIME,
        FOREIGN KEY (id_current_session) REFERENCES current_session (id_current_session),
        FOREIGN KEY (id_event) REFERENCES event (id_event)
    )
''')

persons_conn.commit()
persons_conn.close()



server_files_conn = sqlite3.connect('server_files.db')
server_files_create = server_files_conn.cursor()

server_files_create.execute('''
    CREATE TABLE files (
        id_files INTEGER PRIMARY KEY,
        filename TEXT,
        size INTEGER,
        file_path TEXT,
        created_time DATETIME,
        updated_time DATETIME,
        status INTEGER
    )
''')

server_files_create.execute('''
    CREATE TABLE files_activity (
        id_files_activity INTEGER PRIMARY KEY,
        id_person INTEGER,
        id_files INTEGER,
        type_interactions TEXT,
        timestamp DATETIME,
        FOREIGN KEY (id_person) REFERENCES person (id_person),
        FOREIGN KEY (id_files) REFERENCES files (id_files)
    )
''')


server_files_conn.commit()
server_files_conn.close()