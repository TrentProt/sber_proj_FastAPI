from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.cases import crud
from src.core.dependencies import verify_access_token
from src.core.models import db_helper

router = APIRouter(tags=['Cases'], prefix='/cases')

@router.get('/{case_id}')
async def get_case(
        case_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.get_case(
        case_id=case_id,
        session=session
    )


@router.get('/{case_id}/start')
async def start_case(
        case_id: int,
        _: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.start_case(
        case_id=case_id,
        session=session
    )


@router.post('/{case_id}/finish')
async def finish_case(
        case_id: int,
        payload: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    user_id = int(payload.get('sub'))
    return await crud.finish_case(
        case_id=case_id,
        user_id=user_id,
        session=session
    )