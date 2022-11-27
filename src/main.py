from multiprocessing import Process
from multiprocessing.sharedctypes import Array

import telemetry
from storages import IpcChannel
from config import Settings


if __name__ == '__main__':
    DeviceIpcData = Array(IpcChannel, [(1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0)], lock=True)
    args = (
        DeviceIpcData,
        Settings.TELEMETRY_DELAY,
        Settings.TELEMETRY_LOG,
    )
    telemetry_process = Process(name='telemetry', target=telemetry.run, args=args)
    telemetry_process.run()

    telemetry_process.join()