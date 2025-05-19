from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.static_test import crud
from src.core.dependencies import verify_access_token
from src.core.models import db_helper


router = APIRouter(tags=['Static tests'], prefix='/static_test')


@router.get('/{test_id}/start')
async def get_questions(
        test_id: int,
        _: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.start_test(
        test_id=test_id,
        session=session
    )


@router.get('/{test_id}/question/{q_num}')
async def get_question_answers(
        test_id: int,
        q_num: int,
        _: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.get_question(
        q_num=q_num,
        test_id=test_id,
        session=session
    )
