from multiprocessing import Process
from multiprocessing.sharedctypes import Array

import uvicorn
from fastapi import FastAPI

import src.telemetry
from src.storages.ipc_storage import IpcChannel
from src.config import Settings

from src.api.endpoints.endpoints import api_router


def get_fastapi_app():
    fastapi_app = FastAPI(
        title='Power supply API',
        docs_url='/swagger',
        openapi_url='/openapi',
        version='0.1.0'
    )
    fastapi_app.include_router(api_router)
    return fastapi_app

fastapi_app = get_fastapi_app()


if __name__ == '__main__':
    DeviceIpcData = Array(IpcChannel, [(1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0)], lock=True)

    telemetry_process = Process(
        name='telemetry', target=src.telemetry.run, args=(DeviceIpcData,)
    )
    telemetry_process.start()

    uvicorn.run(
        'main:fastapi_app',
        host=Settings.HTTP_API_SERVER,
        port=Settings.HTTP_API_PORT,
        reload=True,
        log_level='debug'
    )

    telemetry_process.join()
