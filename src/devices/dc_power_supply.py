from devices import Device, DeviceError
from enum import Enum


class DC_power_suply(Device):

    class CMDS(Enum):
        CHANNEL_ON:str = 'on'
        CHANNEL_OFF:str = 'off'
        GET_DATA:str = 'get_data'

    def process_command(self, command:str, params:dict):
        if command == self.CMDS.CHANNEL_ON.value:
            pass
        elif command == self.CMDS.CHANNEL_OFF.value:
            pass
        elif command == self.CMDS.GET_DATA.value:
            pass
        else:
            raise DeviceError(f'Unexpected command "{command}" was received')

    def _channel_on(self, num: int, current: int, voltage: int):
        pass

    def _channel_off(self, num: int):
        pass

    def _get_data(self):
        pass