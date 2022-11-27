from abc import ABC, abstractmethod

from src.hardware.error import HardwareError


class Storage(ABC):
    @abstractmethod
    def set(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError()


class StorageError(HardwareError):
    pass

