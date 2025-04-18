from fastapi import HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.auth.helpers import create_access_token, create_refresh_token
from src.users.schemas import CreateUserSchema, LoginUserSchema
from src.core.models.users import Users
from src.auth.utils import encode_jwt, decode_jwt

import bcrypt

async def create_user(session: AsyncSession, user_in: CreateUserSchema):
    user = user_in.model_dump()
    if user['password1'] != user['password2']:
        raise HTTPException(status_code=401, detail='Пароли не совпадают')
    user_to_save = Users(
        number=user["number"],
        password=bcrypt.hashpw(user['password1'].encode('utf-8'), bcrypt.gensalt(rounds=4)).decode('utf-8'),
    )
    session.add(user_to_save)
    await session.commit()
    return {'ok': True, 'used_id': user_to_save.id}


async def login_user(session: AsyncSession, user_in: LoginUserSchema, response: Response):
    query = select(Users).where(Users.number == user_in.number)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Пользователь с таким именем не найден"
        )
    if not bcrypt.checkpw(user_in.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(
            status_code=401,
            detail="Пароль введен неверно"
        )
    access_token = create_access_token(user)
    response.set_cookie('access_token', access_token)
    refresh_token = create_refresh_token(user)
    response.set_cookie('refresh_token', refresh_token)
    return {'access_token': access_token,
            'refresh_token': refresh_token}


