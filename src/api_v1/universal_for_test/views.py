from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.universal_for_test import crud
from src.api_v1.universal_for_test.schemas import GetTestSchema
from src.core.models import db_helper

router = APIRouter(tags=['Random tests', 'Static tests'], prefix='/tests')


@router.get('/{test_id}')
@cache(expire=60*60*8)
async def get_test(
        test_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> GetTestSchema:
    return await crud.get_test(
        test_id=test_id,
        session=session
    )