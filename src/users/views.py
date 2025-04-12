from fastapi import APIRouter
from src.users.schemas import CreateUserSchema
from src.users import crud

router = APIRouter(tags=['Users'])


@router.post('/users')
def create_user(user: CreateUserSchema):
    return crud.create_user(user_in=user)