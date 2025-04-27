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
    stmt = select(Topics).options(joinedload(Topics.section_topic))
    result = await session.execute(stmt)
    topics = result.unique().scalars().all()

    topics_data = []
    for topic in topics:
        topic_dict = {
            'id': topic.id,
            'name': topic.name,
            'description': topic.description,
            'sections_topic': []
        }
        for section in topic.section_topic:
            tests_count = await session.scalar(
                select(func.count(TestsName.id))
                .where(
                    TestsName.section_topic_id == section.id
                )
            ) or 0
            solved_count = 0
            if user_id:
                solved_count = await session.scalar(
                    select(func.count(distinct(UserAttempts.test_id)))
                    .join(UserAttempts.test)
                    .where(
                        and_(
                            UserAttempts.user_id == int(user_id),
                            UserAttempts.score == 100,
                            TestsName.section_topic_id == section.id
                        )
                    )
                )
            section_data = {
                'id': section.id,
                'title': section.title,
                'description': section.description,
                'tests_count': tests_count,
                'solved_tests': solved_count
            }
            topic_dict['sections_topic'].append(section_data)
        topics_data.append(topic_dict)
    return topics_data


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

