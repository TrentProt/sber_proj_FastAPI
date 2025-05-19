from typing import Union, List

from pydantic import BaseModel


class HistoryTestSchema(BaseModel):
    id: int
    title: str
    time_execution: int
    score: int

class CreateProfile(BaseModel):
    first_name: str
    last_name: str
    middle_name: Union[str, None] = None


class UpdateProfile(CreateProfile):
    bio: Union[str, None] = None


class GetProfile(UpdateProfile):
    id: int
    history_test: List[HistoryTestSchema]

class OkResponse(BaseModel):
    ok: bool
    message: str
