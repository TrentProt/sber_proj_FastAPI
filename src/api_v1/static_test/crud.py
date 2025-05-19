from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.models import TestsName, Questions, Answers


async def start_test(
        test_id: int,
        session: AsyncSession
):
    stmt = select(TestsName).where(
        and_(
            TestsName.id == test_id,
            TestsName.type_test == 'static'
        )
    )
    result = (await session.execute(stmt)).scalar()
    if not result:
        raise HTTPException(status_code=404, detail='Page not found')
    return {
        'ok': True,
        'message': 'Questions ready'
    }


async def get_question(
        q_num: int,
        test_id: int,
        session: AsyncSession
):
    stmt_check = select(TestsName.count_question).where(
        TestsName.id == test_id
    )
    check_count = (await session.execute(stmt_check)).scalar()

    if check_count < q_num:
        raise HTTPException(status_code=404, detail='Page not found')

    stmt_q = select(Questions).options(joinedload(Questions.answers)).where(
        Questions.test_id == test_id
    ).limit(1).offset(q_num-1)
    question = (await session.execute(stmt_q)).scalar()

    response_data = {
        'q_num': q_num,
        'question_text': question.question_text,
        'answers': [
            {
                'id': answer.id,
                'answer_text': answer.answer_text
            }
            for answer in question.answers
        ]
    }
    return response_data




