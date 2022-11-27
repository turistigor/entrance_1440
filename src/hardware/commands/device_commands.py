from typing import Optional

from hardware.commands.command import Command, DEVICE_CMDS, CommandError
from hardware.devices.device import Device
from storages.storage import Storage


class BaseCommand:
    def __init__(self, device: Device):
        self._device = device


class ChannelOn(BaseCommand, Command):
    def run(self, ch_num:int, current:float, voltage:float):
        self._device.channel_on(ch_num, current, voltage)


class ChannelOff(BaseCommand, Command):
    def run(self, ch_num:int):
        self._device.channel_off(ch_num)


class GetData(BaseCommand, Command):
    def run(self, storage:Optional[Storage]):
        data = self._device.get_data()
        storage.set(data)

        return data


def create_command(cmd_type:DEVICE_CMDS, device:Device):
    if cmd_type == DEVICE_CMDS.CHANNEL_ON:
        return ChannelOn(device)
    elif cmd_type == DEVICE_CMDS.CHANNEL_OFF:
        return ChannelOff(device)
    elif cmd_type == DEVICE_CMDS.GET_DATA:
        return GetData(device)
    raise CommandError(f'Command {cmd_type.value} is not supported now')