from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.cases import crud
from src.api_v1.cases.schemas import GetCaseSchema, StartCaseSchema, OkResponse
from src.core.dependencies import verify_access_token
from src.core.models import db_helper

router = APIRouter(tags=['Cases'], prefix='/cases')

@router.get('/{case_id}')
@cache(expire=60*60*4)
async def get_case(
        case_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> GetCaseSchema:
    return await crud.get_case(
        case_id=case_id,
        session=session
    )


@router.get('/{case_id}/start')
@cache(expire=60*60*2)
async def start_case(
        case_id: int,
        _: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> StartCaseSchema:
    return await crud.start_case(
        case_id=case_id,
        session=session
    )


@router.post('/{case_id}/finish')
async def finish_case(
        case_id: int,
        payload: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> OkResponse:
    user_id = int(payload.get('sub'))
    return await crud.finish_case(
        case_id=case_id,
        user_id=user_id,
        session=session
    )