from typing import List

from pydantic import BaseModel


class ChannelModel(BaseModel):
    num: int
    current: float
    voltage: float
    update_dt: str


class DataModel(BaseModel):
    channels: List[ChannelModel]
