from typing import List, Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.tests import crud
from src.core.dependencies import verify_access_token
from src.core.models import db_helper



router = APIRouter(tags=['Tests'], prefix='/tests')

@router.get('/{test_id}')
async def get_section_and_tests_of_the_section(
        test_id: int,
        token_payload: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.get_test(
        test_id=test_id,
        payload=token_payload,
        session=session
    )