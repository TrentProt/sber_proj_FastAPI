from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import UserAttempts, TestsName, Users


async def get_leaderboard_crud(
        user_id: int,
        session: AsyncSession
):
    stmt = select(
        Users.id,
        Users.username,
        func.sum(UserAttempts.score).label('score'),
    ).join(
        UserAttempts.user
    ).join(
        UserAttempts.test
    ).where(
        TestsName.type_test == 'random'
    ).group_by(
        Users.id,
        Users.username,
    ).order_by(
        func.sum(UserAttempts.score).desc()
    )

    result = await session.execute(stmt)
    all_users = result.all()

    leaderboard = [
        {'place': place, 'user_id': row.id, 'username': row.username, 'score': row.score}
        for place, row in enumerate(all_users, start=1)
    ]

    current_user_data = None

    for user in leaderboard:
        if user['user_id'] == user_id:
            current_user_data = user
            break

    top_users = leaderboard[:3]

    return {
        'top_users': top_users,
        'current_user': current_user_data,
    }
