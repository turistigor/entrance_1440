from abc import ABC, abstractmethod
from enum import Enum

from src.hardware.error import HardwareError


class DEVICE_CMDS(Enum):
    CHANNEL_ON:str = 'on'
    CHANNEL_OFF:str = 'off'
    GET_DATA:str = 'get_data'


class Command(ABC):
    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError()


class CommandError(HardwareError):
    pass
