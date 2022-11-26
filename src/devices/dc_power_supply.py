from enum import Enum

from devices import Device, DeviceError, Protocol, ProtocolError


class PowerSupplyCmds(Enum):
    CHANNEL_ON:str = 'on'
    CHANNEL_OFF:str = 'off'
    GET_DATA:str = 'get_data'


class PowerSupply(Device):
    CHANNEL_NUM_MIN: int = 1
    CHANNEL_NUM_MAX: int = 4

    CURRENT_MIN: float = 0
    CURRENT_MAX: float = 6.2

    VOLTAGE_MIN: float = 0
    VOLTAGE_MAX: float = 32

    def __init__(self, protocol: Protocol):
        self._protocol = protocol

    def process_command(self, command:PowerSupplyCmds, params:dict):
        if command == PowerSupplyCmds.CHANNEL_ON:
            return self._channel_on(**params)
        elif command == PowerSupplyCmds.CHANNEL_OFF:
            return self._channel_off(**params)
        elif command == PowerSupplyCmds.GET_DATA:
            return self._get_data(**params)

        raise DeviceError(f'Command "{command.value}" is not suppoted now')

    @classmethod
    def _check_channel_num(cls, ch_num):
        if ch_num < cls.CHANNEL_NUM_MIN or ch_num > cls.CHANNEL_NUM_MAX:
            raise DeviceError(f'Forbiden channel number {ch_num}')

    @classmethod
    def _check_current(cls, current):
        if current < cls.CURRENT_MIN or current > cls.CURRENT_MAX:
            raise DeviceError(f'Forbiden current value {current}')

    @classmethod
    def _check_voltage(cls, current):
        if current < cls.VOLTAGE_MIN or current > cls.VOLTAGE_MIN:
            raise DeviceError(f'Forbiden current value {current}')

    def _channel_on(self, ch_num:int, current:float, voltage: float):
        self._check_channel_num(ch_num)
        self._check_current(current)
        self._check_voltage(voltage)

        self._protocol.set_current(ch_num, current)
        self._protocol.set_voltage(ch_num, voltage)
        self._protocol.channel_on(ch_num)

    def _channel_off(self, ch_num:int):
        self._check_channel_num(ch_num)
        self._protocol.channel_off(ch_num)

    def _get_data(self) -> dict:
        res = {}
        for cn_num in range(self.CHANNEL_NUM_MIN, self.CHANNEL_NUM_MAX+1):
            res[cn_num] = self.protocol.get_channel_data(cn_num)

        return res
