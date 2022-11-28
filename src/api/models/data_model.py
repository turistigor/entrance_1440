from typing import List

from pydantic import BaseModel


class ChannelModel(BaseModel):
    number: int
    current: float
    voltage: float
    dt_update: str


class DataModel(BaseModel):
    channels: List[ChannelModel]
