
import sys
import glob
import serial
import serial.tools.list_ports

AJUST_VID = 1240
AJUST_PID = 221
AJUST_BAUDRATE = 115200

def get_ajust_serial_ports():
    ports = serial.tools.list_ports.comports()

    for port in sorted(ports):
        if(port.vid == AJUST_VID) and (port.pid == AJUST_PID):
            print("{}: {} [{}:{}]".format(
                port, port.interface, port.vid, port.pid))

            return port.device

    return None
