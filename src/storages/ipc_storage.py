from ctypes import Structure, c_char_p, c_ushort, c_float
from ctypes import Array

from storages.storage import Storage, StorageError


class IpcChannel(Structure):
    _fields_ = [('num', c_ushort), ('current', c_float), ('voltage', c_float), ('update_dt', c_char_p)] 


class IpcStorage(Storage):
    def __init__(self, shared_data: Array):
        if not shared_data:
            raise StorageError('Unexpected IPC data structure')

        self._shared_data = shared_data

    def set(self, data: dict):
        for ch_num, channel in data.items():
            self._shared_data[ch_num - 1].current = channel[0]
            self._shared_data[ch_num - 1].voltage = channel[1]
            self._shared_data[ch_num - 1].update_dt = channel[2].encode()

    def get(self):
        return {
            i:(ch.current, ch.voltage, ch.update_dt)
            for i, ch in enumerate(self._shared_data)
        }