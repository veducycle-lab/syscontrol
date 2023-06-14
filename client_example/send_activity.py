import socket
import sqlite3
import datetime
import psutil
import win32gui
import win32process
import win32con
import keyboard
import time

def get_server_ip():
    conn = sqlite3.connect("local_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT ip_server FROM server_recover")
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def check_credentials(login, password):
    ip_server = get_server_ip()
    if ip_server:
        for port in range(25678, 25980):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.connect((ip_server, port))
                    conn = sqlite3.connect("persons.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT id_person, login, psswd FROM person_login_psswd WHERE login = ? AND psswd = ?", (login, password))
                    result = cursor.fetchone()
                    conn.close()
                    if result is not None:
                        id_person = result[0]
                        id_pc = get_pc_id()
                        if id_person and id_pc:
                            session_id = get_current_session_id(id_person, id_pc)
                            if session_id:
                                process_request(session_id)
                                return True
                except ConnectionRefusedError:
                    pass
    return False


def get_current_session_id(id_person, id_pc):
    conn = sqlite3.connect("persons.db")
    cursor = conn.cursor()
    today = datetime.date.today().strftime("%d.%m.%Y")
    cursor.execute("SELECT id_current_session FROM current_session WHERE id_person = ? AND id_pc = ? AND session_date = ?", (id_person, id_pc, today))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None


def get_pc_id():
    conn = sqlite3.connect("local_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id_pc FROM pc_recover")
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None


def process_request(session_id):
    conn = sqlite3.connect("persons.db")
    cursor = conn.cursor()
    is_browser = False
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in ['firefox.exe', 'chrome.exe', 'msedge.exe']:
            is_browser = True
            break
    table_name = "session_stats_browse" if is_browser else "session_stats_app"
    window_size = get_window_size()
    event_type = None
    event_data = None
    time_start = None
    time_end = None
    if is_double_click():
        event_type = 1
        event_data = get_click_coordinates()
        time_start = get_current_time()
        time_end = None
    if event_type == 1 and is_app_in_focus():
        event_type = 2
        event_data = get_click_coordinates()
        time_end = get_current_time()
    if event_type == 2 and is_typing_active():
        event_type = 3
        event_data = get_keyboard_input()
        time_end = get_current_time()
    query = "INSERT INTO {} (id_current_session, name_process, windows_size, id_event, event_data, time_start, time_end) VALUES (?, ?, ?, ?, ?, ?, ?)".format(table_name)
    cursor.execute(query, (session_id, get_process_name(), window_size, event_type, event_data, time_start, time_end))
    conn.commit()
    conn.close()


def get_window_size():
    hwnd = win32gui.GetForegroundWindow()
    rect = win32gui.GetWindowRect(hwnd)
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]
    return f"{width}x{height}"

def is_double_click():
    return keyboard.is_double_click()

def get_click_coordinates():
    coordinates = keyboard.get_mouse_position()
    return f"[x:{coordinates[0]},y:{coordinates[1]}]"

def get_current_time():
    return time.strftime("%H:%M:%S")

def is_app_in_focus():
    hwnd = win32gui.GetForegroundWindow()
    return hwnd != 0

def is_typing_active():
    return keyboard.is_pressed()

def get_keyboard_input():
    text = keyboard.get_typed_strings()
    return " ".join(text)

def get_process_name():
    hwnd = win32gui.GetForegroundWindow()
    pid = win32process.GetWindowThreadProcessId(hwnd)
    handle = win32process.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid[1])
    return win32process.GetModuleFileNameEx(handle, 0)

