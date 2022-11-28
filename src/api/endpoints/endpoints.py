from fastapi import APIRouter
from starlette import status

from src.api.models.data_model import DataModel


api_router = APIRouter()


@api_router.get(
    '/getdata',
    status_code=status.HTTP_200_OK,
    response_model=DataModel
)
async def get_data():
    return {
        'channels': [
            {'number':1, 'current': 2, 'voltage':3, 'dt_update': 'adasd'}
        ],
    }
