from datetime import datetime, timedelta
from typing import Union

import jwt

from src.core.config import settings

def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes
    ):
    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
        token: Union[str, bytes],
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm
        ):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded

