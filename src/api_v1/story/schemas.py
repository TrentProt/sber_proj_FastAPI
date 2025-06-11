from typing import Union

from pydantic import BaseModel


class Position(BaseModel):
    bottom: str
    right: str


class Size(BaseModel):
    width: int
    height: int


class Color(BaseModel):
    top: str
    bottom: str


class GetStories(BaseModel):
    id: int
    title: str
    body: list
    img_url: Union[str, None]
    position: Position
    size: Size
    color: Color