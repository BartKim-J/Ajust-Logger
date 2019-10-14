# -*- coding:utf-8 -*-
import sys
import time
import threading
import glob
import serial
import serial.tools.list_ports

from Modules.ajustAPI import ajustLogin, ajustLogUpdate
from Modules.serialPort import ReaderThread, Protocol
from Modules.ajustPort import get_ajust_serial_ports, AJUST_BAUDRATE


def ajust_parsing_data(data):
    data = data.decode()

    StartCode = data[0:1]
    device_SN = int(data[1:3], 16)
    device_Type = int(data[3:4], 16)
    device_Group = device_Type
    device_Count = int(data[4:8], 16)
    EndCode = data[8:9]

    logData = {
        "device_SN": device_SN,
        "device_Type": device_Type,
        "device_Count": device_Count,
        "group": device_Group,
    }
    
    res = ajustLogUpdate(logData)


class rawProtocal(Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.running = True

    def connection_lost(self, exc):
        self.transport = None

    def data_received(self, data):
        ajust_parsing_data(data)

    def write(self, data):
        self.transport.write(data)

    def isDone(self):
        return self.running


def serialThreadInit():
    PORT = get_ajust_serial_ports()

    serialInstance = serial.serial_for_url(
        PORT, baudrate=AJUST_BAUDRATE, timeout=5)
    with ReaderThread(serialInstance, rawProtocal) as p:
        while p.isDone():
            time.sleep(1)


def main():
    res = ajustLogin()
    while(res != 200):
        print("Retry Login to Server...")
        time.sleep(3)
        res = ajustLogin()

    serialThreadInit()


main()
