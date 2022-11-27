from hardware.devices import Device
from hardware.protocols import  Protocol
from hardware.commands import Command, DEVICE_CMDS, create_command

from config import Settings


class DeviceManager:
    def __init__(
        self, protocol_cls: Protocol, device_cls: Device
    ):
        protocol = protocol_cls(Settings.DEVICE_HOST, Settings.DEVICE_PORT)
        self._device = device_cls(protocol)

    def process_command(self, cmd: DEVICE_CMDS, params:dict):
        cmd:Command = create_command(cmd, self._device)
        return cmd.run(**params)


class HardwareError(Exception):
    pass
