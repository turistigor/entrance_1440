from devices.dc_power_supply import PowerSupply, PowerSupplyCmds
from devices.scpi import Scpi

from config import Settings


class DeviceManager:
    def __init__(self):
        protocol = Scpi(Settings.DEVICE_HOST, Settings.DEVICE_PORT)
        self._device = PowerSupply()

    def process_command(self, cmd: PowerSupplyCmds, params: dict):
        res = self._device.process_command(cmd, params)
        #...