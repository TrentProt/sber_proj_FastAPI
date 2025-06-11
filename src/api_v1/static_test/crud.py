from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api_v1.static_test.schemas import AddAttemptUser
from src.core.models import TestsName, Questions, UserAttempts

from src.core.redis import redis_client

import json

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


async def finish_static_test(
        user_id: int,
        test_id: int,
        data_answers: AddAttemptUser,
        session: AsyncSession
):
    stmt = (
        select(Questions)
        .options(
            joinedload(Questions.answers)
        )
        .where(
            Questions.test_id == test_id
        )
    )
    questions = (await session.execute(stmt)).unique().scalars().all()
    questions_map = {question.id: question for question in questions}

    user_answers_map = {qa.q_num: qa.answer_id for qa in data_answers.qanswers}
    print(user_answers_map)
    correct_count = 0
    redis_results_key = f"user:{user_id}:test:{test_id}:results"
    answer_details = []

    for q_num, answer_id in user_answers_map.items():
        question_id = list(questions_map.keys())[q_num-1]
        question = questions_map.get(question_id)
        correct_answer = next((a for a in question.answers if a.correct), None)
        is_correct = correct_answer and (answer_id == correct_answer.id)

        if is_correct:
            correct_count += 1

        answer_details.append({
            'q_num': q_num,
            'question_id': question_id,
            'answer_id': answer_id,
            'is_correct': is_correct,
            'correct_answer_id': correct_answer.id if correct_answer else None
        })

    total_questions = len(questions)

    if total_questions == 0:
        raise HTTPException(status_code=400, detail='No questions')

    redis_client.setex(redis_results_key, 1200, json.dumps(answer_details))

    score = int((correct_count / total_questions) * 100)

    new_attempt = UserAttempts(
        user_id=user_id,
        test_id=test_id,
        count_correct_answer=correct_count,
        time_execution=data_answers.time_execution,
        score=score
    )
    session.add(new_attempt)
    await session.commit()

    return {
            'ok': True,
            'test_was_passed': True,
            'message': 'Test passed'
            }