import random
from typing import TYPE_CHECKING

from fastapi import HTTPException

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api_v1.tests.service import redis_helper
from src.core.models import TestsName, Questions


async def get_random_questions(
        test_id: int,
        user_id: str,
        section_id: int,
        session: AsyncSession
):
    stmt = select(
        TestsName
    ).options(joinedload(TestsName.questions)).where(
        and_(
            TestsName.id == test_id,
            TestsName.section_topic_id == section_id
        )
    )
    test = (await session.execute(stmt)).unique().scalar_one_or_none()

    if not test:
        raise HTTPException(status_code=404, detail='Page not found')

    all_question_id = [question.id for question in test.questions]

    if not all_question_id:
        raise HTTPException(status_code=404, detail="No questions found")

    if len(all_question_id) < test.count_question:
        raise HTTPException(status_code=400, detail='Not enough questions')

    rndm_questions = random.sample(all_question_id, test.count_question)

    redis_key = f'user:{user_id}:test:{test_id}:questions'
    redis_helper(
        redis_key=redis_key,
        time_expire=3600,
        arg=rndm_questions
    )

    return {
        'ok': True,
        'message': 'Questions ready',
        'question_ids': rndm_questions
    }


async def get_test(
        test_id: int,
        section_id: int,
        session: AsyncSession
):
    stmt = select(TestsName).where(
        and_(
            TestsName.id == test_id,
            TestsName.section_topic_id == section_id
        )
    )
    test = (await session.execute(stmt)).scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail='Page not found')
    return {
        'id': test.id,
        'title': test.title,
        'description': test.description,
        'time_test': test.time_test,
        'questions_count': test.count_question
    }


async def get_qa_for_test(
        question_id: int,
        session: AsyncSession
):
    stmt = select(Questions).options(joinedload(Questions.answers)).where(
        and_(
            Questions.id == question_id,
        )
    )
    question = (await session.execute(stmt)).unique().scalar_one_or_none()

    if not question:
        raise HTTPException(status_code=404, detail='Page not found')

    all_answers = question.answers
    correct_answer_id = [a.id for a in all_answers if a.correct]
    print(correct_answer_id)
    return {
        'id': question.id,
        'question': question.question_text,
        'answers': [],
        'tip': 'Подсказка'
    }
