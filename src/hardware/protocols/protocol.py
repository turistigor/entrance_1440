from abc import ABC, abstractmethod

from src.hardware.error import HardwareError


class Protocol(ABC):
    @abstractmethod
    def set_current(self, ch_num, current):
        raise NotImplementedError()

    @abstractmethod
    def set_voltage(self, ch_num, voltage):
        raise NotImplementedError()

    @abstractmethod
    def channel_on(self, ch_num):
        raise NotImplementedError()

    @abstractmethod
    def channel_off(self, ch_num):
        raise NotImplementedError()

    @abstractmethod
    def get_channel_data(self, ch_num):
        raise NotImplementedError()


class ProtocolError(HardwareError):
    pass

