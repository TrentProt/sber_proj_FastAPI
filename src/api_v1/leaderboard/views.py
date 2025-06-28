from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.leaderboard import crud
from src.api_v1.leaderboard.schemas import LeaderBoardResponseSchemas
from src.core.dependencies import verify_access_token
from src.core.models import db_helper

router = APIRouter(tags=['Leaderboard'], prefix='/leaderboard')

@router.get('/')
async def get_leaderboard(
        token_payload: dict = Depends(verify_access_token),
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> LeaderBoardResponseSchemas:
    user_id = int(token_payload.get('sub'))
    return await crud.get_leaderboard_crud(
        user_id=user_id,
        session=session
    )