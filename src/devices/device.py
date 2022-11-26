from abc import ABC, abstractmethod
from typing import Optional


class Device(ABC):
    @abstractmethod
    def process_command(self, *args, **kwargs) -> Optional[dict] :
        raise NotImplementedError()


class DeviceError(Exception):
    pass
