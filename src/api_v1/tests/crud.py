import json
import random

from fastapi import HTTPException

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api_v1.tests.schemas import AddUserAttempt
from src.api_v1.tests.service import redis_helper
from src.core.models import TestsName, Questions, UserAttempts
from src.core.redis import redis_client


async def get_random_questions(
        test_id: int,
        user_id: str,
        session: AsyncSession
):
    stmt_check = select(func.count()).where(
        and_(
            UserAttempts.user_id == int(user_id),
            UserAttempts.test_id == test_id
        )
    )
    attempts_count = (await session.execute(stmt_check)).scalar()
    if attempts_count > 0:
        return {
            'ok': True,
            'test_was_passed': True,
            'message': 'Test was passed'
        }

    redis_key = f'user:{user_id}:test:{test_id}:questions'

    if redis_client.exists(redis_key):
        return {
            'ok': True,
            'test_was_passed': False,
            'message': 'Questions already have'
        }

    stmt = select(
        TestsName
    ).options(joinedload(TestsName.questions)).where(
        TestsName.id == test_id,
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

    redis_helper(
        redis_key=redis_key,
        time_expire=7200,
        arg=rndm_questions
    )
    return {
        'ok': True,
        'test_was_passed': False,
        'message': 'Questions ready'
    }


async def get_test(
        test_id: int,
        session: AsyncSession
):
    stmt = select(TestsName).where(
        and_(
            TestsName.id == test_id,
            TestsName.type_test == 'random'
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
        q_num: int,
        user_id: str,
        test_id: int,
        session: AsyncSession
):
    redis_key = f"user:{user_id}:test:{test_id}:questions"

    if not redis_client.exists(redis_key):
        raise HTTPException(status_code=400, detail='Not add in redis')

    question_ids = redis_client.lrange(redis_key, 0, -1)

    if not question_ids or q_num > len(question_ids):
        raise HTTPException(status_code=404, detail="Question not found")

    question_id = int(question_ids[q_num - 1])

    stmt = select(Questions).options(joinedload(Questions.answers)).where(
        and_(
            Questions.test_id == test_id,
            Questions.id == question_id
        )
    )

    question = (await session.execute(stmt)).unique().scalar_one_or_none()

    if not question:
        raise HTTPException(status_code=404, detail='Page not found')

    all_answers = question.answers
    correct_answer_id = [a for a in all_answers if a.correct]
    wrong_answer_id = [a for a in all_answers if not a.correct]
    select_3_wrong_1_correct = random.sample(wrong_answer_id, 3) + correct_answer_id
    random.shuffle(select_3_wrong_1_correct)
    return {
        'q_num': int(q_num),
        'question_id': question.id,
        'question': question.question_text,
        'answers': [
            {
                'id': answer.id,
                'answer_text': answer.answer_text.strip()
            }
            for answer in select_3_wrong_1_correct
        ],
        'tip': 'Подсказка'
    }


async def finish_test(
        test_id: int,
        user_id: int,
        data_answers: AddUserAttempt,
        session: AsyncSession
):
    stmt_check = select(func.count()).where(
        and_(
            UserAttempts.user_id == int(user_id),
            UserAttempts.test_id == test_id
        )
    )
    attempts_count = (await session.execute(stmt_check)).scalar()
    if attempts_count > 0:
        return {
            'ok': True,
            'test_was_passed': True,
            'message': 'Test was passed'
        }

    redis_key = f"user:{user_id}:test:{test_id}:questions"

    if not redis_client.exists(redis_key):
        raise HTTPException(status_code=400, detail='Test not started or expired')

    question_ids = [int(qid) for qid in redis_client.lrange(redis_key, 0, -1)]

    if not question_ids:
        raise HTTPException(status_code=400, detail='No questions found')

    stmt = (
        select(Questions)
        .options(
            joinedload(Questions.answers)
        )
        .where(
            Questions.id.in_(question_ids),
            Questions.test_id == test_id
        )
    )
    questions = (await session.execute(stmt)).unique().scalars().all()

    questions_map = {question.id: question for question in questions}
    correct_count = 0
    redis_results_key = f"user:{user_id}:test:{test_id}:results"
    answer_details = []
    user_answers_map = {qa.q_num: qa.answer_id for qa in data_answers.qanswers}

    for q_num, answer_id in user_answers_map.items():
        question_id = question_ids[q_num - 1]
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

    total_questions = len(question_ids)

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

    try:
        redis_client.delete(redis_key)
    except Exception:
        pass

    return {
            'ok': True,
            'test_was_passed': True,
            'message': 'Test passed'
            }


async def get_result_test(
        test_id: int,
        user_id: int,
        session: AsyncSession
):
    redis_key = f"user:{user_id}:test:{test_id}:results"

    if not redis_client.exists(redis_key):
        raise HTTPException(status_code=404, detail="Results expired or not found")

    answers_data = redis_client.get(redis_key)
    if not answers_data:
        raise HTTPException(
            status_code=404,
            detail="Have not data"
        )

    stmt = select(
        UserAttempts.score,
        UserAttempts.time_execution,
        UserAttempts.count_correct_answer
    ).where(
        and_(
            UserAttempts.user_id == user_id,
            UserAttempts.test_id == test_id
        )
    )
    result_db = (await session.execute(stmt)).first()

    if not result_db:
        raise HTTPException(status_code=404, detail="Attempt not found")

    results_form_redis = json.loads(answers_data)
    redis_client.delete(redis_key)
    response_data = {
        'test_id': test_id,
        'count_correct_answer': result_db.count_correct_answer,
        'count_question': len(results_form_redis),
        'score': result_db.score,
        'time_execution': result_db.time_execution,
        'data_answers': []
    }

    sorted_answers = sorted(results_form_redis, key=lambda x: x['q_num'])
    question_ids = [q['question_id'] for q in sorted_answers]

    stmt_qa = select(Questions).options(
        joinedload(Questions.answers)
    ).where(
        Questions.id.in_(question_ids)
    )
    questions = (await session.execute(stmt_qa)).unique().scalars().all()
    questions_map = {q.id: q for q in questions}

    for answer in sorted_answers:
        question = questions_map.get(answer['question_id'])

        correct_answer = next((a for a in question.answers if a.id == answer['correct_answer_id']), None)
        user_answer = next((a for a in question.answers if a.id == answer['answer_id']), None)

        response_data['data_answers'].append({
            'q_num': int(answer['q_num']),
            'question_text': question.question_text,
            'user_answer': {
                'id': int(answer['answer_id']),
                'answer_text': user_answer.answer_text
            },
            'is_correct': bool(answer['is_correct']),
            'correct_answer': {
                'id': int(answer['correct_answer_id']),
                'correct_answer_text': correct_answer.answer_text
            }
        })

    return response_data