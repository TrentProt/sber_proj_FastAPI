import os
import uuid
from pathlib import Path
from typing import Union

from fastapi import HTTPException, UploadFile

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.models.users import UserAttempts
from src.core.models.tests import Topics, TestsName, SectionsTopic


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
SECTION_TOPIC_IMG_DIR = BASE_DIR / "src" / "static" / "images" / "sections_topics"
SECTION_TOPIC_IMG_DIR.mkdir(parents=True, exist_ok=True)


async def get_topics_and_sections_crud(
        user_id: Union[str, None],
        session: AsyncSession
):
    topics_stmt = select(Topics).options(joinedload(Topics.section_topic))
    topics_result = await session.execute(topics_stmt)
    topics = topics_result.unique().scalars().all()

    sections_id = [section.id for topic in topics for section in topic.section_topic]

    test_count_stmt = select(
        TestsName.section_topic_id,
        func.count(TestsName.id).label('test_count')
    ).where(
        TestsName.section_topic_id.in_(sections_id)
    ).group_by(
        TestsName.section_topic_id
    )

    test_count = (await session.execute(test_count_stmt)).all()
    test_count_map = {section_id: count for section_id, count in test_count}

    solved_count_map = {}
    if user_id:
        solved_count_stmt = select(
            TestsName.section_topic_id,
            func.count(UserAttempts.test_id).label('solved_test')
        ).join(
            UserAttempts, UserAttempts.test_id == TestsName.id
        ).where(
            UserAttempts.user_id == int(user_id),
            UserAttempts.score >= 75,
            TestsName.section_topic_id.in_(sections_id)
        ).group_by(
            TestsName.section_topic_id
        )
        solved_count = (await session.execute(solved_count_stmt)).all()
        solved_count_map = {section_id: count for section_id, count in solved_count}

    response = []
    for topic in topics:
        topic_data = {
            'id': topic.id,
            'name': topic.name,
            'description': topic.description,
            'sections_topic': []
        }
        for section in topic.section_topic:
            section_data = {
                'id': section.id,
                'title': section.title,
                'description': section.description,
                'icon': section.img_url if section.img_url else '',
                'test_count': test_count_map.get(section.id, 0),
                'solved_count': solved_count_map.get(section.id, 0) if user_id else 0
            }
            topic_data['sections_topic'].append(section_data)
        response.append(topic_data)
    return response


async def get_section_and_tests(
    user_id: Union[str, None],
    section_topic_id: int,
    session: AsyncSession
):
    stmt = (
        select(SectionsTopic)
        .options(joinedload(SectionsTopic.test))
        .where(SectionsTopic.id == section_topic_id)
    )
    result = await session.execute(stmt)
    section = result.unique().scalar_one_or_none()

    if not section:
        raise HTTPException(status_code=404, detail='Page not found')

    solved_test_count = 0
    solved_question_map = {}
    if user_id:
        solved_count_stmt = select(
            func.count(UserAttempts.test_id)
        ).where(
            and_(
                UserAttempts.user_id == int(user_id),
                UserAttempts.score >= 75
            )
        )
        solved_test_count = (await session.execute(solved_count_stmt)).scalar()
        # ========================
        solved_question_stmt = select(
            TestsName.id,
            UserAttempts.count_correct_answer
        ).join(
            TestsName.user_attempt
        ).where(
            UserAttempts.user_id == int(user_id)
        )
        solved_question = (await session.execute(solved_question_stmt)).all()
        solved_question_map = {test_id: count_correct_question for test_id, count_correct_question
                               in solved_question}

    section_data = {
        'id': section.id,
        'title': section.title,
        'description': section.description,
        'count_solved': solved_test_count,
        'count_tests': len(section.test),
        'theory': '?',
        'tests': []
    }

    for test in section.test:
        test_data = {
            'id': test.id,
            'title': test.title,
            'description': test.description,
            'type_test': test.type_test,
            'status': '?',
            'count_solved': solved_question_map.get(test.id, 0),
            'count_questions': test.count_question
        }
        section_data['tests'].append(test_data)

    return section_data


async def upload_image_section_topic(
        section_topic_id: int,
        file: UploadFile,
        session: AsyncSession
):
    stmt = select(SectionsTopic).where(SectionsTopic.id == section_topic_id)
    result = await session.execute(stmt)
    section_topic = result.scalar_one_or_none()

    if not section_topic:
        raise HTTPException(status_code=404, detail='Page not found')

    file_ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{file_ext}"
    file_path = SECTION_TOPIC_IMG_DIR / filename

    content = await file.read()
    with open(file_path, "wb") as image:
        image.write(content)

    section_topic.img_url = f"/static/images/story/{filename}"
    await session.commit()
    await session.refresh(section_topic)
    return {
        "status": "success",
        "message": "Image uploaded successfully",
        "img_url": section_topic.img_url
    }


