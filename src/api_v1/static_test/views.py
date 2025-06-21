from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.static_test import crud
from src.api_v1.static_test.schemas import OkStatus, GetQuestionSchema, TestPassed, ResultTestSchema
from src.core.dependencies import verify_access_token
from src.core.models import db_helper


router = APIRouter(tags=['Static tests'], prefix='/static_test')


@router.get('/{test_id}/start')
async def get_questions(
        test_id: int,
        _: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> OkStatus:
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
) -> GetQuestionSchema:
    return await crud.get_question(
        q_num=q_num,
        test_id=test_id,
        session=session
    )


@router.post('/{test_id}/question/{q_num}')
async def add_answer(
        test_id: int,
        q_num: int,
        answer_id: int,
        token_payload: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> OkStatus:
    user_id = int(token_payload.get('sub'))
    return await crud.add_answers(
        test_id=test_id,
        q_num=q_num,
        answer_id=answer_id,
        user_id=user_id,
        session=session
    )


@router.post('/{test_id}/finish')
async def finish_test(
        test_id: int,
        time_execution: int,
        token_payload: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> TestPassed:
    user_id = int(token_payload.get('sub'))
    return await crud.finish_test(
        user_id=user_id,
        time_execution=time_execution,
        test_id=test_id,
        session=session
    )

@router.get('/{test_id}/result')
async def result_test(
        test_id: int,
        token_payload: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> ResultTestSchema:
    user_id = int(token_payload.get('sub'))
    return await crud.result_test(
        test_id=test_id,
        user_id=user_id,
        session=session
    )