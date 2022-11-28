from fastapi import APIRouter, Request, Body, HTTPException
from starlette import status

from src.api.models.data_model import DataModel
from src.api.models.channel_on_model import ChannelOnModel, ChannelOffModel
from src.api.logic import get_current_data, channel_turn
from src.hardware.error import HardwareError


api_router = APIRouter()


@api_router.get(
    '/getdata',
    status_code=status.HTTP_200_OK,
    response_model=DataModel
)
async def get_data(request: Request):
    shared_data = request.app.extra['extra']['shared_data']
    return get_current_data(shared_data)


@api_router.post('/channelon', status_code=status.HTTP_200_OK)
async def channel_on(data:ChannelOnModel=Body(...)):
    try:
        channel_turn(data.num, True, data.current, data.voltage)
    except HardwareError as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )


@api_router.post('/channeloff', status_code=status.HTTP_200_OK)
async def channel_off(data:ChannelOffModel=Body(...)):
    try:
        channel_turn(data.num, False)
    except HardwareError as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )
