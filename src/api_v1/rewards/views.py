from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.rewards import crud
from src.api_v1.rewards.schemas import GetAllRewards, GetAllUserRewards
from src.core.dependencies import verify_access_token
from src.core.models import db_helper

router = APIRouter(tags=['Rewards'], prefix='/rewards')

@router.get('/')
@cache(expire=60*60*2)
async def get_all(
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> List[GetAllRewards]:
    return await crud.get_all_rewards(
        session=session
    )


@router.get('/user')
async def get_all_user_rewards(
        token_payload: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> GetAllUserRewards:
    user_id = int(token_payload.get('sub'))
    return await crud.get_all_user_rewards(
        user_id=user_id,
        session=session
    )


# @router.get('/user/{topic_id}')
# async def get_user_reward_in_topic(
#         topic_id: int,
#         token_payload: dict = Depends(verify_access_token),
#         session: AsyncSession = Depends(db_helper.session_dependency)
# ):
#     user_id = int(token_payload.get('sub'))
#     return await crud.get_user_reward_in_topic(
#         topic_id=topic_id,
#         user_id=user_id,
#         session=session
#     )
