
import wmi

c = wmi.WMI()
operating_systems = c.Win32_OperatingSystem()
for os in operating_systems:
    print("Серийный номер операционной системы: {}".format(os.SerialNumber))

disks = c.Win32_LogicalDisk()
for disk in disks:
        print("Серийный номер диска C: {}".format(disk.VolumeSerialNumber))

import ctypes

def get_volume_serial_number(drive_path):
    serial_number = None
    if drive_path:
        drive_path += ':\\'
        serial_number = ctypes.c_ulonglong(0)
        file_system_name = ctypes.create_unicode_buffer(1024)
        max_component_length = ctypes.c_ulonglong(0)
        file_system_flags = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetVolumeInformationW(
            ctypes.c_wchar_p(drive_path),
            None,
            0,
            ctypes.pointer(serial_number),
            ctypes.pointer(max_component_length),
            ctypes.pointer(file_system_flags),
            file_system_name,
            ctypes.sizeof(file_system_name)
        )
    return serial_number.value

serial_number_c_drive = get_volume_serial_number('C')
print(serial_number_c_drive)