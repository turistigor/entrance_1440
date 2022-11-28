from fastapi import APIRouter, Request
from starlette import status

from src.api.models.data_model import DataModel
from src.api.logic.get_current_data import get_current_data


api_router = APIRouter()


@api_router.get(
    '/getdata',
    status_code=status.HTTP_200_OK,
    response_model=DataModel
)
async def get_data(request: Request):
    shared_data = request.app.extra['extra']['shared_data']
    return get_current_data(shared_data)

