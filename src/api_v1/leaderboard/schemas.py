from typing import List

from pydantic import BaseModel

class LeaderBoardSchema(BaseModel):
    place: int
    user_id: int
    username: str
    score: int


class LeaderBoardResponseSchemas(BaseModel):
    top_users: List[LeaderBoardSchema]
    current_user: LeaderBoardSchema