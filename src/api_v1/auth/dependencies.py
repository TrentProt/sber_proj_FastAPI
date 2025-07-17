from datetime import datetime

from zoneinfo import ZoneInfo

from fastapi import HTTPException, Request
from jwt import ExpiredSignatureError

from src.api_v1.auth.utils import decode_jwt


MOSCOW_TZ = ZoneInfo("Europe/Moscow")

def refresh_user_access_token(request: Request):
    refresh_token = request.cookies.get('refresh_token')

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        payload = decode_jwt(token=refresh_token)
        current_time = datetime.now(MOSCOW_TZ).timestamp()
        exp = payload.get("exp")

        if current_time > exp:
            raise ExpiredSignatureError

        return payload

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail=f"Refresh token expired")

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid refresh_token")

