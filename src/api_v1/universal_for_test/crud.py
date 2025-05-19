from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import TestsName


async def get_test(
        test_id: int,
        session: AsyncSession
):
    stmt = select(TestsName).where(
        TestsName.id == test_id
    )
    test = (await session.execute(stmt)).scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail='Page not found')
    return {
        'id': test.id,
        'title': test.title,
        'type_test': test.type_test,
        'description': test.description,
        'time_test': test.time_test,
        'questions_count': test.count_question
    }
