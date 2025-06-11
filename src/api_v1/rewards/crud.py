from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.models import Rewards, UserReward, Topics


async def get_all_rewards(
        session: AsyncSession
):
    stmt = select(Rewards)
    result = (await session.execute(stmt)).scalars().all()
    return result


async def get_all_user_rewards(
        user_id: int,
        session: AsyncSession
):
    stmt_topic = select(Topics.id, Topics.name)
    topics = (await session.execute(stmt_topic)).all()
    topics_map = {topic[0]:topic[1] for topic in topics}

    stmt = select(UserReward).options(
        joinedload(UserReward.reward)
    ).where(
        UserReward.user_id == user_id
    )
    rewards = (await session.execute(stmt)).scalars().all()
    return [
        {
            'id': reward.reward.id,
            'reward': reward.reward.name,
            'description': reward.reward.description,
            'image_url': reward.reward.image_url,
            'topic': topics_map[reward.topic_id]
        }
        for reward in rewards
    ]


async def get_user_reward_in_topic(
        topic_id: int,
        user_id: int,
        session: AsyncSession
):

    stmt = select(UserReward).options(
        joinedload(UserReward.reward), joinedload(UserReward.topic)
    ).where(
        and_(
            UserReward.user_id == user_id,
            UserReward.topic_id == topic_id
        )
    )
    result = (await session.execute(stmt)).scalars().all()
    return [
        {
        'topic_id': reward.topic_id
        }
        for reward in result
    ]