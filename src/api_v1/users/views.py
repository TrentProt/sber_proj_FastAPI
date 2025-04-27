from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.users.schemas import CreateProfile, UpdateProfile, GetProfile, OkResponse
from src.core.dependencies import verify_access_token
from src.core.models import db_helper
from src.api_v1.users import crud

router = APIRouter(tags=['Users'], prefix='/users')


@router.get('/profile')
async def get_profile_user(
        token_payload: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> GetProfile:
    return await crud.profile_user(session=session, payload=token_payload)


@router.post('/profile/create')
async def create_profile_user(
        profile: CreateProfile,
        token_payload: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> OkResponse:
    return await crud.create_profile(profile=profile, payload=token_payload, session=session)


@router.put('/profile/update')
async def update_profile_user(
    profile: UpdateProfile,
    token_payload: dict = Depends(verify_access_token),
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> OkResponse:
    return await crud.update_profile(profile_update=profile, payload=token_payload, session=session)

