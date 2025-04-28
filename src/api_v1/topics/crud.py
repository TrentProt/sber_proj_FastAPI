from typing import Union

from fastapi import HTTPException

from sqlalchemy import select, func, and_, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.models.users import UserAttempts
from src.core.models.tests import Topics, TestsName, SectionsTopic


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
            UserAttempts.score == 100,
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

    section_data = {
        'id': section.id,
        'title': section.title,
        'description': section.description,
        'tests': section.test
    }

    return section_data

