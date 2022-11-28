from datetime import datetime
from typing import Optional

from src.config.settings import Settings
from src.hardware.protocols.scpi import Scpi 
from src.hardware.devices.power_supply import PowerSupply
from src.hardware.commands.device_commands import \
    DEVICE_CMDS, ChannelOn, ChannelOff, create_command


def get_current_data(shared_data):
    channels = []
    for ch in shared_data:
        update_dt = datetime.fromtimestamp(ch.update_dt)
        channels.append({
            'num': ch.num,
            'current': ch.current,
            'voltage': ch.voltage,
            'update_dt': update_dt.isoformat()
        })
    return {
        'channels': channels
    }

def channel_turn(ch_num:int, on:bool, current:Optional[float]=None, voltage:Optional[float]=None):
    protocol = Scpi(
        Settings.DEVICE_HOST, Settings.DEVICE_PORT, Settings.SCPI_DELIMITER
    )
    device = PowerSupply(protocol)

    if on:
        cmd: ChannelOn = create_command(DEVICE_CMDS.CHANNEL_ON, device)
        cmd.run(ch_num, current, voltage)
    else:
        cmd: ChannelOff = create_command(DEVICE_CMDS.CHANNEL_OFF, device)
        cmd.run(ch_num)
