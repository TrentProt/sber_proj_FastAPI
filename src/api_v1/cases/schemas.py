from pydantic import BaseModel

class GetCaseSchema(BaseModel):
    id: int
    title: str
    description: str
    icon: str


class StartCaseSchema(BaseModel):
    id: int
    prompt: str


class OkResponse(BaseModel):
    ok: bool
    message: str