from src.api_v1.auth.utils import encode_jwt
from src.core.config import settings


TOKEN_TYPE_FIELD = 'type'
ACCESS_TOKEN_TYPE = 'access_token'
REFRESH_TOKEN_TYPE = 'refresh_token'

def create_jwt(
        token_type: str,
        token_data: dict,
        expire_minutes: int,
    ):
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes
    )

def create_access_token(user_id: int):
    jwt_payload = {
        'sub': str(user_id)
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes
    )

def create_refresh_token(user_id: int):
    jwt_payload = {
        'sub': str(user_id)
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.auth_jwt.refresh_token_expire_minutes
    )