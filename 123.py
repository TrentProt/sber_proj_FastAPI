import asyncio

import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.core.models.users import Users, Profiles
from src.core.models import db_helper
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.schemas import CreateUserSchema


# async def create_user(session: AsyncSession, user: CreateUserSchema):
#     user = user.model_dump()
#     if user['password1'] == user['password2']:
#         user_to_save = Users(
#             number=user["number"],
#             password=bcrypt.hashpw(user['password1'].encode('utf-8'), bcrypt.gensalt(rounds=4)).decode('utf-8'),
#         )
#     session.add(user_to_save)
#     await session.commit()
#     return {'ok': True, 'used_id': user_to_save.id}


async def get_user_by_id(session: AsyncSession, user_id: int):
    stmt = select(Users).where(Users.id == user_id)
    result = await session.scalars(stmt)
    for user in result:
        print(user.number)

async def create_user_profile(session: AsyncSession, user_id: int, first_name: str, last_name: str):
    profile = Profiles(user_id=user_id, first_name=first_name, last_name=last_name)
    session.add(profile)
    await session.commit()
    return 'ok'

async def get_user_profile(session: AsyncSession, user_id: int):
    stmt = select(Users).options(joinedload(Users.profile)).where(Users.id == user_id)
    user = await session.scalar(stmt)
    print(user.profile.first_name)


async def main():
    async with db_helper.session_factory() as session:
        await get_user_profile(session=session, user_id=1)

if __name__ == '__main__':
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except RuntimeError as e:
        if "Event loop is closed" not in str(e):
            raise
    finally:
        loop.close()