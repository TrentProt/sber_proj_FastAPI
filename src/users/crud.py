from src.users.schemas import CreateUserSchema


def create_user(user_in: CreateUserSchema):
    user = user_in.model_dump()
    return {
        'success': True,
        'user': user['password1']
    }