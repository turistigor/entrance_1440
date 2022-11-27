from abc import ABC, abstractmethod

from hardware import HardwareError


class Device(ABC):
    @abstractmethod
    def channel_on(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def channel_off(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def _get_data(self, *args, **kwargs) -> dict:
        raise NotImplementedError()


class DeviceError(HardwareError):
    pass
