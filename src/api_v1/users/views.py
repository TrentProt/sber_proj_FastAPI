from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import db_helper
from src.api_v1.users.dependencies import verify_access_token
from src.api_v1.users.schemas import CreateUserSchema, LoginUserSchema
from src.api_v1.users import crud

router = APIRouter(tags=['Users'], prefix='/users')


@router.get('/profile')
async def profile_user(
        token_payload: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.profile_user(session=session, payload=token_payload)



