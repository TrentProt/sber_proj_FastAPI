from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.schemas import CreateUserSchema, LoginUserSchema
from src.core.models.users import Users
import bcrypt

async def create_user(session: AsyncSession, user_in: CreateUserSchema):
    user = user_in.model_dump()
    if user['password1'] != user['password2']:
        raise HTTPException(status_code=401, detail='Пароли не совпадают')
    user_to_save = Users(
        username=user["username"],
        password=bcrypt.hashpw(user['password1'].encode('utf-8'), bcrypt.gensalt(rounds=4)).decode('utf-8'),
        bio=None
    )
    session.add(user_to_save)
    await session.commit()
    return {'ok': True, 'used_id': user_to_save.id}


async def login_user(session: AsyncSession, user_in: LoginUserSchema):
    user_login = user_in.model_dump()
    query = select()

