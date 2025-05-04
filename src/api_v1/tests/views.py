from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.tests import crud, service
from src.core.dependencies import verify_access_token
from src.core.models import db_helper



router = APIRouter(tags=['Tests'], prefix='/tests')

@router.get('/{section_id}/{test_id}/start')
async def generate_question_for_test(
        test_id: int,
        section_id: int,
        token_payload: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    user_id = token_payload.get('sub')
    return await crud.get_random_questions(
        test_id=test_id,
        user_id=user_id,
        section_id=section_id,
        session=session
    )


@router.get('/{section_id}/{test_id}')
async def get_test(
        test_id: int,
        section_id: int,
        token_payload: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.get_test(
        test_id=test_id,
        section_id=section_id,
        session=session
    )


@router.get('{test_id}/question/{question_id}')
async def get_question_answers_for_test(
        question_id: int,
        test_id: int,
        token_payload: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.get_qa_for_test(
        question_id=question_id,
        session=session
    )