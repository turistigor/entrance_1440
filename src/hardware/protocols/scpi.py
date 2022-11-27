import socket

from src.hardware.protocols.protocol import Protocol


class Scpi(Protocol):
    def __init__(self, host:str, port: int):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.connect((host, port))

    def __del__(self):
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()
        #FIXME: tmp
        print('Socket was closed')

    @staticmethod
    def set_current(ch_num, current):
        pass

    @staticmethod
    def set_voltage(ch_num, voltage):
        pass

    @staticmethod
    def channel_on(ch_num):
        pass

    @staticmethod
    def channel_off(ch_num):
        pass

    @staticmethod
    def get_channel_data(ch_num):
        pass