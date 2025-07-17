from pydantic import BaseModel, Field, field_validator
import re
from typing import Optional, Union


class CreateUserSchema(BaseModel):
    number: str = Field(min_length=3, max_length=12, examples=['string'])
    password1: str = Field(min_length=3, examples=['string'])
    password2: str

    @field_validator('number')
    def validate_number(cls, v: str) -> str:
        if not re.match(r'^\+?\d{11,12}$', v):
            raise ValueError('Номер должен содержать 11-12 цифр')
        return v

    @field_validator('password1')
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Пароль должен быть не менее 8 символов')
        if not any(c.isupper() for c in v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not any(c.isdigit() for c in v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        return v

    @field_validator('password2')
    def passwords_match(cls, v: str, values) -> str:
        if 'password1' in values.data and v != values.data['password1']:
            raise ValueError('Пароли не совпадают')
        return v

class LoginUserSchema(BaseModel):
    username: str = Field(..., min_length=1, max_length=40)
    password: str = Field(..., min_length=3)

    # @field_validator('user')
    # def validate_number(cls, v: str) -> str:
    #     if not re.match(r'^\+?\d{11,12}$', v):
    #         raise ValueError('Номер должен содержать 11-12 цифр')
    #     return v


class UserSchema(LoginUserSchema):
    id: int


class OkResponse(BaseModel):
    ok: bool
    message: str


class CheckAuth(BaseModel):
    is_authenticated: bool
    user_id: Union[int, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    middle_name: Union[str, None] = None

