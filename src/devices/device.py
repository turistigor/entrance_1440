from abc import ABC, abstractmethod


class Device(ABC):
    @abstractmethod
    def process_command(self, *args, **kwargs):
        raise NotImplementedError()


class DeviceError(Exception):
    pass
