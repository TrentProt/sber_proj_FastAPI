from typing import List

from fastapi import APIRouter, Depends, UploadFile, File

from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.story import crud
from src.api_v1.story.schemas import GetStories
from src.core.models import db_helper



router = APIRouter(tags=['Story'], prefix='/story')

@router.post('/{story_id}')
async def upload_image(
        story_id: int,
        file: UploadFile = File(...),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.upload_image_story(story_id=story_id, file=file, session=session)


@router.get('/')
async def get_stories(
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> List[GetStories]:
    return await crud.get_all_story(session=session)