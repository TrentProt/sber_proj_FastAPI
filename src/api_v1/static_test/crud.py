from fastapi import HTTPException
from sqlalchemy import select, and_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

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
    ).limit(1).offset(q_num-1).order_by(Questions.id)
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


async def add_answers(
        user_id: int,
        test_id: int,
        q_num: int,
        answer_id: int,
        session: AsyncSession
):
    stmt = (
        select(Questions)
        .options(
            joinedload(Questions.answers)
        )
        .where(
            Questions.test_id == test_id
        ).limit(1).offset(q_num-1)
    ).order_by(Questions.id)
    question = (await session.execute(stmt)).unique().scalar_one_or_none()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found in this test")

    correct_answer = next((a for a in question.answers if a.correct), None)
    is_correct = correct_answer and (answer_id == correct_answer.id)

    redis_key = f"user:{user_id}:test:{test_id}:answers"
    answer_data = {
        "question_id": question.id,
        "answer_id": answer_id,
        "is_correct": int(is_correct),
        "correct_answer_id": correct_answer.id if correct_answer else None
    }
    await redis_client.hset(redis_key, str(q_num), json.dumps(answer_data))
    await redis_client.expire(redis_key, 7200)

    return {
        'ok': True,
        'message': 'Added answer'
    }


async def finish_test(
        test_id: int,
        user_id: int,
        time_execution: int,
        session: AsyncSession
):
    stmt = select(func.count(Questions.id)).where(
        Questions.test_id == test_id
    )
    count_question = (await session.execute(stmt)).scalar()
    redis_key = f"user:{user_id}:test:{test_id}:answers"
    all_answers = await redis_client.hgetall(redis_key)

    if not all_answers:
        raise HTTPException(status_code=400, detail="No answers found")

    correct_count = 0
    for q_num, answer_json in all_answers.items():
        answer = json.loads(answer_json)
        if answer["is_correct"]:
            correct_count += 1

    score = int((correct_count / count_question) * 100) if correct_count else 0
    new_attempt = UserAttempts(
        user_id=user_id,
        test_id=test_id,
        count_correct_answer=correct_count,
        time_execution=time_execution,
        score=score
    )
    session.add(new_attempt)
    await session.commit()

    return {
        'ok': True,
        'test_was_passed': True,
        'message': 'Test passed'
    }


async def result_test(
        test_id: int,
        user_id: int,
        session: AsyncSession
):
    redis_key = f"user:{user_id}:test:{test_id}:answers"
    all_answers = await redis_client.hgetall(redis_key)
    await redis_client.delete(redis_key)

    if not all_answers:
        raise HTTPException(status_code=400, detail="No answers found")

    stmt = select(Questions).options(joinedload(Questions.answers)).where(
            Questions.test_id == test_id
    ).order_by(Questions.id)
    questions = (await session.execute(stmt)).unique().scalars().all()

    stmt_attempt = select(
        UserAttempts
    ).where(
        and_(
            UserAttempts.user_id == user_id,
            UserAttempts.test_id == test_id
        )
    ).order_by(desc(UserAttempts.complete_at)).limit(1)
    result_attepmt = (await session.execute(stmt_attempt)).scalar_one_or_none()

    if not result_attepmt:
        raise HTTPException(status_code=404, detail="Test attempt not found")

    data_answers = []
    for q_num, question in enumerate(questions, start=1):
        answer_json = all_answers.get(str(q_num))

        if answer_json:
            user_answer_data = json.loads(answer_json)
            user_answer = next(
                (a for a in question.answers if a.id == user_answer_data["answer_id"]),
                None
            )
            is_correct = bool(int(user_answer_data["is_correct"]))
        else:
            user_answer = None
            is_correct = False

        correct_answer = next(
            (a for a in question.answers if a.correct),
            None
        )

        data_answers.append({
            "q_num": q_num,
            "question_text": question.question_text,
            "user_answer": {
                "id": user_answer.id if user_answer else None,
                "answer_text": user_answer.answer_text if user_answer else None
            },
            "is_correct": is_correct,
            "correct_answer": {
                "id": correct_answer.id if correct_answer else None,
                "correct_answer_text": correct_answer.answer_text if correct_answer else None
            }
        })
    response_data = {
        'test_id': test_id,
        'count_correct_answer': result_attepmt.count_correct_answer,
        'count_question': len(questions),
        'score': result_attepmt.score,
        'time_execution': result_attepmt.time_execution,
        'data_answers': data_answers
    }

    return response_data