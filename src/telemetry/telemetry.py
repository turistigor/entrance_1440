from time import sleep
from ctypes import Array

from storages.ipc_storage import IpcStorage
from hardware.devices.power_supply import PowerSupply
from hardware.protocols.scpi import Scpi 
from hardware.commands.command import DEVICE_CMDS
from hardware.commands.device_commands import GetData
from hardware.error import HardwareError
from hardware.commands.device_commands import create_command

from config import Settings


def write_log(file_d, data):
    lines = (f'{ch},{params[0]},{params[1]},{params[2]}\n' for ch, params in data.items())
    file_d.writelines(lines)


def run(shared_data:Array):
    storage = IpcStorage(shared_data)
    protocol = Scpi(
        Settings.DEVICE_HOST, Settings.DEVICE_PORT, Settings.SCPI_DELIMITER
    )
    device = PowerSupply(protocol)
    cmd:GetData = create_command(DEVICE_CMDS.GET_DATA, device)

    with open(Settings.TELEMETRY_LOG,'wt') as f:
        while True:
            try:
                device_data = cmd.run(storage)
            except HardwareError as err:
                #FIXME: tmp
                print(err)

            write_log(f, device_data)
            sleep(Settings.TELEMETRY_DELAY)
