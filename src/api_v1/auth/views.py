from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.crud import check_auth
from src.api_v1.auth.helpers import create_access_token
from src.core.models import db_helper
from src.api_v1.auth.dependencies import refresh_user_access_token
from src.api_v1.auth.schemas import (
    LoginUserSchema,
    CheckAuth, OkResponse
)
from src.api_v1.auth import crud

router = APIRouter(tags=['Auth'], prefix='/auth')


@router.post('/registration')
async def create_user(
        user: CreateUserSchema,
        session: AsyncSession = Depends(db_helper.session_dependency),
    ) -> OkResponse:
    return await crud.create_user(session=session, user_in=user)


@router.post('/login')
async def login_user(
        user: LoginUserSchema,
        response: Response,
        session: AsyncSession = Depends(db_helper.session_dependency)
    ) -> OkResponse:
    return await crud.login_user(session=session, user_in=user, response=response)


@router.post('/refresh_token', response_model_exclude_none=True)
async def auth_refresh_jwt(
        response: Response,
        user: dict = Depends(refresh_user_access_token),
) -> OkResponse:
    token = create_access_token(user['sub'])
    response.delete_cookie('access_token', secure=True, httponly=True, samesite="lax")
    response.set_cookie('access_token', token, secure=True, httponly=True, samesite="lax")
    return OkResponse(
        ok=True,
        message="Refresh success"
    )


@router.get('/check_auth', response_model_exclude_none=True)
async def check_auth_user_and_get_datauser(
        request: Request,
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> CheckAuth:
    access_token = request.cookies.get("access_token")
    if not access_token:
        return CheckAuth(
            is_authenticated=False,
            user_id=None,
            first_name=None,
            last_name=None,
            middle_name=None
        )
    return await check_auth(access_token=access_token, session=session)


@router.post('/logout', response_model_exclude_none=True)
async def auth_refresh_jwt(
        response: Response
):
    response.delete_cookie('access_token', secure=True, httponly=True, samesite="lax")
    response.delete_cookie('refresh_token', secure=True, httponly=True, samesite="lax")
    return {
        'ok':True,
        'message':"Logout success"
    }