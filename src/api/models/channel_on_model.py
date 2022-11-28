from pydantic import BaseModel


class ChannelOnModel(BaseModel):
    num: int
    current: float
    voltage: float


class ChannelOffModel(BaseModel):
    num: int