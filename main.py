from multiprocessing import Process
from multiprocessing.sharedctypes import Array
from ctypes import Structure, c_ushort, c_float

import uvicorn
from fastapi import FastAPI

import src.telemetry
from src.config.settings import Settings

from src.api.endpoints.endpoints import api_router


class IpcChannel(Structure):
    _fields_ = [('num', c_ushort), ('current', c_float), ('voltage', c_float), ('update_dt', c_float)]


device_ipc_data = Array(IpcChannel, [(1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0)], lock=True)


def get_fastapi_app():
    fastapi_app = FastAPI(
        title='Power supply API',
        docs_url='/swagger',
        openapi_url='/openapi',
        version='0.1.0',
        extra = {'shared_data': device_ipc_data}
    )
    fastapi_app.include_router(api_router)
    return fastapi_app


if __name__ == '__main__':

    telemetry_process = Process(
        name='telemetry', target=src.telemetry.run, args=(device_ipc_data,)
    )
    telemetry_process.start()

    uvicorn.run(
        get_fastapi_app,
        host=Settings.HTTP_API_SERVER,
        port=Settings.HTTP_API_PORT,
        log_level='debug',
        factory=True
    )

    telemetry_process.join()
