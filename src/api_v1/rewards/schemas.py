from pydantic import BaseModel

class GetAllRewards(BaseModel):
    id: int
    name: str
    description: str
    image_url: str