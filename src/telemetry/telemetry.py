from time import sleep
from datetime import datetime
from multiprocessing.sharedctypes import Array

from src.storages.ipc_storage import IpcStorage
from src.hardware.devices.power_supply import PowerSupply
from src.hardware.protocols.scpi import Scpi 
from src.hardware.commands.command import DEVICE_CMDS
from src.hardware.commands.device_commands import GetData
from src.hardware.error import HardwareError
from src.hardware.commands.device_commands import create_command

from src.config.settings import Settings


def write_log(file_d, data):
    lines = (f'{ch},{params[0]},{params[1]},{params[2]}\n' for ch, params in data.items())
    file_d.writelines(lines)
    file_d.flush()


def is_log_overflow(log_start:datetime) -> bool:
    log_life_time = (datetime.now() - log_start).total_seconds() / 60
    return log_life_time >= Settings.TELEMETRY_TIME_MIN


def run(shared_data:Array):
    storage = IpcStorage(shared_data)
    protocol = Scpi(
        Settings.DEVICE_HOST, Settings.DEVICE_PORT, Settings.SCPI_DELIMITER
    )
    device = PowerSupply(protocol)
    cmd:GetData = create_command(DEVICE_CMDS.GET_DATA, device)

    try:
        while True:
            log_start = datetime.now()
            
            with open(Settings.TELEMETRY_LOG, 'wt') as f:
                while not is_log_overflow(log_start):
                    device_data = cmd.run(storage)
                    write_log(f, device_data)
                    sleep(Settings.TELEMETRY_DELAY_SEC)
    except HardwareError as err:
        print(err)
