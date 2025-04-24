from fastapi import HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.api_v1.users.schemas import CreateProfile, UpdateProfile
from src.core.models.users import Users, Profiles


async def create_profile(profile: CreateProfile,  payload: dict, session: AsyncSession):
    user_id = int(payload.get('sub'))
    print(profile.model_dump())
    if not user_id:
        raise HTTPException(status_code=401, detail='Invalid token payload')
    profile_to_save = Profiles(
        user_id=user_id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        middle_name=profile.middle_name,
    )
    session.add(profile_to_save)
    await session.commit()
    return {'ok': True}


async def profile_user(session: AsyncSession, payload: dict):
    user_id = int(payload.get('sub'))
    stmt = select(Users).options(joinedload(Users.profile)).where(Users.id == user_id)
    user = await session.scalar(stmt)
    return {'ok': user.profile.first_name}


async def update_profile(profile: UpdateProfile, payload: dict, session: AsyncSession):
    user_id = int(payload.get('sub'))
    if not user_id:
        raise HTTPException(status_code=401, detail='Invalid token payload')
    stmt = select(Users).options(joinedload(Users.profile)).where(Users.id == user_id)
    pass