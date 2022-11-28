from datetime import datetime

from src.storages.storage import Storage, StorageError


class IpcStorage(Storage):
    def __init__(self, shared_data):
        if not shared_data:
            raise StorageError('Unexpected IPC data structure')

        self._shared_data = shared_data

    def set(self, data: dict):
        for i, ch in enumerate(self._shared_data):
            ch.current = data[i+1][0]
            ch.voltage = data[i+1][1]
            update_dt = datetime.fromisoformat(data[i+1][2])
            ch.update_dt = update_dt.timestamp()

    def get(self):
        return {
            i:(ch.current, ch.voltage, ch.update_dt)
            for i, ch in enumerate(self._shared_data)
        }
