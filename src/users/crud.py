from fastapi import HTTPException

from src.users.schemas import CreateUserSchema


def create_user(user_in: CreateUserSchema):
    user = user_in.model_dump()
    if user['password1'] == user['password2']:
        return {
            'success': True,
            'user': user['password1']
        }
    raise HTTPException(status_code=401, detail='Incorrect password')