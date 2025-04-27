from fastapi import APIRouter, Depends

from typing import List, Union

from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.topics import crud
from src.api_v1.topics.dependencies import get_id_user_or_none_from_cookie
from src.api_v1.topics.schemas import TopicOut
from src.core.models import db_helper



router = APIRouter(tags=['Topics and Sections of the topics'])

@router.get('/topics')
async def get_topics_and_sections_for_main_page(
        user_id: Union[str, None] = Depends(get_id_user_or_none_from_cookie),
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> List[TopicOut]:
    return await crud.get_topics_and_sections_crud(user_id=user_id, session=session)


@router.get('/section/{section_topic_id}')
async def get_section_and_tests_in_section(
        section_topic_id: int,
        user_id: Union[str, None] = Depends(get_id_user_or_none_from_cookie),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.get_section_and_tests(user_id=user_id, section_topic_id=section_topic_id, session=session)