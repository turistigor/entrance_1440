from time import sleep

from src.hardware.devices.device import Device, DeviceError 
from src.hardware.protocols.protocol import Protocol


class PowerSupply(Device):
    CHANNEL_NUM_MIN: int = 1
    CHANNEL_NUM_MAX: int = 4

    CURRENT_MIN: float = 0
    CURRENT_MAX: float = 6.2

    VOLTAGE_MIN: float = 0
    VOLTAGE_MAX: float = 32

    def __init__(self, protocol: Protocol):
        self._protocol = protocol

    @classmethod
    def _check_channel_num(cls, ch_num:float):
        if ch_num < cls.CHANNEL_NUM_MIN or ch_num > cls.CHANNEL_NUM_MAX:
            raise DeviceError(f'Forbiden channel number {ch_num}')

    @classmethod
    def _check_current(cls, current:float):
        if current < cls.CURRENT_MIN or current > cls.CURRENT_MAX:
            raise DeviceError(f'Forbiden current value {current}')

    @classmethod
    def _check_voltage(cls, current):
        if current < cls.VOLTAGE_MIN or current > cls.VOLTAGE_MAX:
            raise DeviceError(f'Forbiden voltage value {current}')

    def channel_on(self, ch_num:int, current:float, voltage: float):
        self._check_channel_num(ch_num)
        self._check_current(current)
        self._check_voltage(voltage)

        self._protocol.set_current(ch_num, current)
        sleep(0.1)
        self._protocol.set_voltage(ch_num, voltage)
        sleep(0.1)
        self._protocol.channel_on(ch_num)

    def channel_off(self, ch_num:int):
        self._check_channel_num(ch_num)
        self._protocol.channel_off(ch_num)

    def get_data(self) -> dict:
        res = {}
        for cn_num in range(self.CHANNEL_NUM_MIN, self.CHANNEL_NUM_MAX+1):
            res[cn_num] = self._protocol.get_channel_data(cn_num)

        return res
