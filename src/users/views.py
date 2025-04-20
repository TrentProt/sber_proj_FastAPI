from typing import Optional

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.helpers import create_access_token
from src.core.models import db_helper
from src.users.dependencies import verify_access_token, refresh_user_access_token
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


@router.get('/profile')
async def profile_user(
        token_payload: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.profile_user(session=session, payload=token_payload)

@router.post('/refresh')
async def auth_refresh_jwt(
        response: Response,
        user: dict = Depends(refresh_user_access_token),
):
    token = create_access_token(user['sub'])
    response.set_cookie('access_token', token)
    return {'access_token': token}

