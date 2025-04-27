from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.models import TestsName


async def get_test(
        test_id: int,
        payload: dict,
        session: AsyncSession
):
    stmt = select(TestsName).options(joinedload(TestsName.question)).where(TestsName.id == test_id)
    test = (await session.execute(stmt)).scalar()
    return {
        'id': test.id,
        'title': test.title,
        'time_test': test.time_test,
        'questions_count': len(test.question)
    }

