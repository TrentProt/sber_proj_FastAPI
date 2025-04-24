from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.helpers import create_access_token
from src.core.models import db_helper
from src.api_v1.auth.dependencies import refresh_user_access_token
from src.api_v1.auth.schemas import CreateUserSchema, LoginUserSchema
from src.api_v1.auth import crud

router = APIRouter(tags=['Auth'], prefix='/auth')

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


@router.post('/refresh')
async def auth_refresh_jwt(
        response: Response,
        user: dict = Depends(refresh_user_access_token),
):
    token = create_access_token(user['sub'])
    response.delete_cookie('access_token', secure=True, httponly=True, samesite="lax")
    response.set_cookie('access_token', token, secure=True, httponly=True, samesite="lax")
    return {'access_token': token}
