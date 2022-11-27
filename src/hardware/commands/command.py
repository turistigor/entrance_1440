from abc import ABC, abstractmethod
from enum import Enum

from hardware.commands.device_commands import \
    ChannelOn, ChannelOff, GetData, Device

from hardware import HardwareError


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


def create_command(cmd_type:DEVICE_CMDS, device:Device):
    if cmd_type == DEVICE_CMDS.CHANNEL_ON:
        return ChannelOn(device)
    elif cmd_type == DEVICE_CMDS.CHANNEL_OFF:
        return ChannelOff(device)
    elif cmd_type == DEVICE_CMDS.GET_DATA:
        return GetData(device)
    raise CommandError(f'Command {cmd_type.value} is not supported now')