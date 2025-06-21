from pydantic import BaseModel

class GetAllRewards(BaseModel):
    id: int
    name: str
    description: str
    image_url: str


class GetAllUserRewards(BaseModel):
    id: int
    reward: str
    description: str
    image_url: str
    topic_id: int
    topic: str