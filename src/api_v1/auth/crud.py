from fastapi import HTTPException, Response
from pyexpat.errors import messages

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.api_v1.auth.helpers import create_access_token, create_refresh_token
from src.api_v1.auth.schemas import CreateUserSchema, LoginUserSchema
from src.api_v1.auth.utils import decode_jwt
from src.core.models import Profiles
from src.core.models.users import Users

import bcrypt

async def create_user(session: AsyncSession, user_in: CreateUserSchema):
    user = user_in.model_dump()
    if user['password1'] != user['password2']:
        raise HTTPException(status_code=401, detail='Пароли не совпадают')
    if user["number"][:2] == '+7':
        number = user['number'].replace('+7', '8')
    else:
        number = user['number']
    user_to_save = Users(
        number=number,
        password=bcrypt.hashpw(user['password1'].encode('utf-8'), bcrypt.gensalt(rounds=4)).decode('utf-8'),
    )
    session.add(user_to_save)
    await session.commit()
    return {
        'ok': True,
        'used_id': user_to_save.id,
        'message': 'Registration success'
    }


async def login_user(session: AsyncSession, user_in: LoginUserSchema, response: Response):
    if user_in.number[2:] == '+7':
        number = user_in.number.replace('+7', '8')
    else:
        number = user_in.number

    query = select(Users).where(Users.number == number)
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

    access_token = create_access_token(user.id)
    response.set_cookie('access_token', access_token, secure=True, httponly=True, samesite='lax')
    refresh_token = create_refresh_token(user.id)
    response.set_cookie('refresh_token', refresh_token, secure=True, httponly=True, samesite='lax')
    return {'ok': True,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'message': 'Login user success'}


async def check_auth(access_token: str, session: AsyncSession):
    try:
        payload = decode_jwt(access_token)
        user_id = int(payload.get('sub'))
        stmt = select(Profiles).where(Profiles.user_id == user_id)
        result = await session.execute(stmt)
        profile = result.scalar_one_or_none()

        if not profile:
            return {'is_authenticated': False}

        return {
            'is_authenticated': True,
            'user_id': profile.user_id,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'middle_name': profile.middle_name
        }
    except Exception:
        return {'is_authenticated': False}