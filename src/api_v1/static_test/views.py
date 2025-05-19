from fastapi import APIRouter, Depends, UploadFile, File

from typing import List, Union

from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.topics import crud
from src.api_v1.topics.dependencies import get_id_user_or_none_from_cookie
from src.api_v1.topics.schemas import TopicOut, SectionForTests
from src.core.models import db_helper



router = APIRouter(tags=['Topics and Sections for main'])