from pydantic import BaseModel

class GetTestSchema(BaseModel):
    id: int
    title: str
    type_test: str
    description: str
    time_test: int
    questions_count: int