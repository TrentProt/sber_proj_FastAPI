from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    username: str
    password1: str
    password2: str

class LoginUserSchema(BaseModel):
    username: str
    password: str