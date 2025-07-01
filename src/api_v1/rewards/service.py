from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import TestsName, UserAttempts, UserReward
from src.core.models.tests import SectionsTopic, Topics


class RewardService:
    def __init__(self, session: AsyncSession, redis_client):
        self.session = session
        self.redis = redis_client

    async def check_and_add_reward(self, topic_id: int, user_id: int):
        total_tests = await self.get_cache_test_count(topic_id)
        passed_tests = await self.get_passed_tests(
            user_id=user_id,
            topic_id=topic_id
        )
        reward_id = self.calculate_reward(
            passed=passed_tests,
            total_test=total_tests
        )

        if not reward_id:
            return {
                'reward_id': None
            }

        if not await self.has_reward(
            user_id=user_id,
            topic_id=topic_id,
            reward_id=reward_id
        ):
            await self.add_reward(
                user_id=user_id,
                topic_id=topic_id,
                reward_id=reward_id
            )
            return reward_id
        return None


    async def get_cache_test_count(self, topic_id: int):
        cache_key = f'topic:{topic_id}:count_test'
        count_test_cache = await self.redis.get(cache_key)

        if count_test_cache:
            return int(count_test_cache)

        count = await self.get_count_from_db(topic_id)

        if count:
            await self.redis.setex(cache_key, 60 * 60 * 8, str(count))

        return count

    async def get_count_from_db(self, topic_id: int):
        stmt_count_tests = select(
            func.count(TestsName.id)
        ).join(
            TestsName.section_topic
        ).join(
            SectionsTopic.topic
        ).where(
            and_(
                Topics.id == topic_id,
                TestsName.type_test == 'random'
            )
        )
        count_tests_in_topic = (await self.session.execute(
            stmt_count_tests
        )).scalar_one_or_none()
        return count_tests_in_topic

    async def get_passed_tests(self, user_id: int, topic_id: int):
        stmt_count_passed_tests = select(
            func.count(UserAttempts.id)
        ).join(
            UserAttempts.test
        ).where(
            and_(
                UserAttempts.topic_id == topic_id,
                UserAttempts.score >= 75,
                UserAttempts.user_id == user_id,
                TestsName.type_test == 'random'
            )
        )
        count_passed_tests = (await self.session.execute(
            stmt_count_passed_tests
        )).scalar_one_or_none()
        return count_passed_tests

    @staticmethod
    def calculate_reward(passed: int, total_test: int):
        percent = (passed / total_test) * 100
        if percent >= 90: return 4
        if percent >= 60: return 3
        if percent >= 30: return 2
        return None

    async def has_reward(self, user_id: int, topic_id: int, reward_id: int):
        stmt = select(
            UserReward
        ).where(
            and_(
                UserReward.user_id == user_id,
                UserReward.reward_id == reward_id,
                UserReward.topic_id == topic_id
            )
        )
        has_reward = (await self.session.execute(stmt)).scalar_one_or_none()
        return has_reward is not None

    async def add_reward(self, user_id: int, topic_id: int, reward_id: int):
        new_reward = UserReward(
            user_id=user_id,
            topic_id=topic_id,
            reward_id=reward_id
        )
        self.session.add(new_reward)
        await self.session.commit()
