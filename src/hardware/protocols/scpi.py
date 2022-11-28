import socket
from datetime import datetime

from src.hardware.protocols.protocol import Protocol, ProtocolError


class Scpi(Protocol):
    def __init__(self, host:str, port: int, delimiter:str):
        self._delimiter = delimiter
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.connect((host, port))

    def __del__(self):
        self._socket.close()

    def set_current(self, ch_num, current):
        cmd = f':SOURce{ch_num}:CURRent {current}'
        self._socket.sendall(cmd.encode())

    def set_voltage(self, ch_num, voltage):
        cmd = f':SOURce{ch_num}:VOLTage {voltage}'
        self._socket.sendall(cmd.encode())

    def channel_on(self, ch_num):
        cmd = f':OUTPut{ch_num} ON'
        self._socket.sendall(cmd.encode())

    def channel_off(self, ch_num):
        cmd = f':OUTPut{ch_num} OFF'
        self._socket.sendall(cmd.encode())

    def get_channel_data(self, ch_num):
        cmd = f':MEASure{ch_num}:ALL?'
        self._socket.sendall(cmd.encode())
        data = self._socket.recv(32)

        if not data:
            raise ProtocolError('Connection is closed by device')

        current, voltage, __ = data.decode().split(self._delimiter)
        return (float(current), float(voltage), datetime.utcnow().isoformat())
