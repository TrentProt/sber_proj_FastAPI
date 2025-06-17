from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import Cases, UserAttemptsCase


async def get_case(
        case_id: int,
        session: AsyncSession
):
    stmt = select(
        Cases
    ).where(
        Cases.id == case_id
    )
    case = (await session.execute(stmt)).scalar()

    if not case:
        return HTTPException(status_code=404, detail='Page not found')
    return {
        'id': case.id,
        'title': case.title,
        'description': case.description,
        'icon': case.icon,
    }


async def start_case(
        case_id: int,
        session: AsyncSession
):
    stmt = select(
        Cases.id, Cases.prompt
    ).where(
        Cases.id == case_id
    )
    case = (await session.execute(stmt)).first()

    if not case:
        return HTTPException(status_code=404, detail='Page not found')

    if not case.prompt:
        raise HTTPException(status_code=400, detail='Case has no prompt')

    return {
        'id': case.id,
        'prompt': case.prompt
    }


async def finish_case(
        case_id: int,
        user_id: int,
        session: AsyncSession
):
    new_attempt_case = UserAttemptsCase(
        user_id=user_id,
        case_id=case_id
    )
    session.add(new_attempt_case)
    await session.commit()
    return {
        'ok': True,
        'message': 'Case complete'
    }