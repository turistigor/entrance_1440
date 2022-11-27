from time import sleep
from ctypes import Array

from storages import IpcStorage
from hardware import PowerSupply, Scpi, create_command, \
    DEVICE_CMDS, GetData, HardwareError

from config import Settings


def write_log(file_d, data):
    lines = (f'{ch},{params[0]},{params[1]},{params[2]}' for ch, params in data)
    file_d.writelines(*lines)


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
