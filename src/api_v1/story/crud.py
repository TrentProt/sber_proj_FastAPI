import os
import uuid
from distutils.util import execute
from pathlib import Path
from typing import TYPE_CHECKING

from fastapi import HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import Story

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
STORY_IMG_DIR = BASE_DIR / "src" / "static" / "images" / "story"
STORY_IMG_DIR.mkdir(parents=True, exist_ok=True)


async def upload_image_story(
        story_id: int,
        file: UploadFile,
        session: AsyncSession
):
    stmt = select(Story).where(Story.id == story_id)
    result = await session.execute(stmt)
    story = result.scalar_one_or_none()

    if not story:
        raise HTTPException(status_code=404, detail='Page not found')

    file_ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{file_ext}"
    file_path = STORY_IMG_DIR / filename

    content = await file.read()
    with open(file_path, "wb") as image:
        image.write(content)

    story.img_url = f"/static/images/story/{filename}"
    await session.commit()
    await session.refresh(story)
    return {
        "status": "success",
        "message": "Image uploaded successfully",
        "img_url": story.img_url
    }


async def get_all_story(session: AsyncSession):
    stmt = select(Story)
    result = await session.execute(stmt)
    stories = result.scalars().all()

    response_data = []
    for story in stories:
        story_data = {
            'id': story.id,
            'title': story.title,
            'body': story.body,
            'img_url': story.img_url if story.img_url else '',
            'position': {
                'top': '15%',
                'left': '10%'
            },
            'size': {
                'width': '70%',
                'height': '60vh'
            }
        }
        response_data.append(story_data)

    return response_data