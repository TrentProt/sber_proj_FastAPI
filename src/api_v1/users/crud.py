from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.api_v1.users.schemas import CreateProfile, UpdateProfile
from src.core.models import UserAttempts, TestsName
from src.core.models.users import Profiles


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
    return {'ok': True, 'message': 'Profile Create'}


async def profile_user(session: AsyncSession, payload: dict):
    user_id = int(payload.get('sub'))
    stmt = select(Profiles).where(Profiles.user_id == user_id)
    result = await session.execute(stmt)
    profile = result.scalar_one_or_none()

    stmt_history = select(
        UserAttempts
    ).options(joinedload(UserAttempts.test)).where(
        UserAttempts.user_id == user_id,
    ).order_by(
        UserAttempts.complete_at.desc()
    ).limit(2)
    history = (await session.execute(stmt_history)).scalars().all()

    response_data = {
        'id': profile.id,
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'middle_name': profile.middle_name,
        'bio': profile.bio,
        'history_test': [
            {
                'id': attempt.test.id,
                'title': attempt.test.title,
                'time_execution': attempt.time_execution,
                'score': attempt.score
            }
            for attempt in history
        ]
    }
    return response_data


async def update_profile(profile_update: UpdateProfile, payload: dict, session: AsyncSession):
    user_id = int(payload.get('sub'))
    if not user_id:
        raise HTTPException(status_code=401, detail='Invalid token payload')
    stmt = select(Profiles).where(Profiles.user_id == user_id)
    result = await session.execute(stmt)
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    update_dict = profile_update.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(profile, field, value)
    await session.commit()
    return {"ok": True, "message": "Profile updated"}