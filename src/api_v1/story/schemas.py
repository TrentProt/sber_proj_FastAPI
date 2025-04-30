from typing import Union

from pydantic import BaseModel


class Position(BaseModel):
    top: str
    left: str


class Size(BaseModel):
    width: str
    height: str


class GetStories(BaseModel):
    id: int
    title: str
    body: str
    img_url: Union[str, None]
    position: Position
    size: Size