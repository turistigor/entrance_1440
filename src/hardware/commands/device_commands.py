from typing import Optional

from hardware import Command, Device
from storages import Storage


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
        data = self._device._get_data()
        storage.set(data)

        return data
