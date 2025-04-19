from typing import Optional

from fastapi import APIRouter, Depends, Response, Cookie, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import db_helper
from src.users.dependencies import verify_access_token
from src.users.schemas import CreateUserSchema, LoginUserSchema
from src.users import crud

router = APIRouter(tags=['Users'], prefix='/users')


@router.post('/registration')
async def create_user(
        user: CreateUserSchema,
        session: AsyncSession = Depends(db_helper.session_dependency,),
    ):
    return await crud.create_user(session=session, user_in=user)


@router.post('/login')
async def login_user(
        user: LoginUserSchema,
        response: Response,
        session: AsyncSession = Depends(db_helper.session_dependency)
    ):
    return await crud.login_user(session=session, user_in=user, response=response)


@router.get('/user/profile')
async def profile_user(
        token_payload: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.profile_user(session=session, payload=token_payload)
