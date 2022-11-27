import socket
from datetime import datetime

from src.hardware.protocols.protocol import Protocol


class Scpi(Protocol):
    def __init__(self, host:str, port: int, delimiter:str):
        self._delimiter = delimiter
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.connect((host, port))

    def __del__(self):
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()
        #FIXME: tmp
        print('Socket was closed')

    def set_current(self, ch_num, current):
        pass

    def set_voltage(self, ch_num, voltage):
        pass

    def channel_on(self, ch_num):
        pass

    def channel_off(self, ch_num):
        pass

    def get_channel_data(self, ch_num):
        cmd = f':MEASure{ch_num}:ALL?\n'
        self._socket.sendall(cmd.encode('utf8'))
        data = str(self._socket.recv(32))

        current, voltage, __ = data.split(self._delimiter)
        return (current, voltage, datetime.utcnow().isoformat())


