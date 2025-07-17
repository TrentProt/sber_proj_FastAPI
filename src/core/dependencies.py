from datetime import datetime

from zoneinfo import ZoneInfo

from jwt import ExpiredSignatureError

from fastapi import HTTPException, Request, Response

from src.api_v1.auth.dependencies import refresh_user_access_token
from src.api_v1.auth.helpers import create_access_token
from src.api_v1.auth.utils import decode_jwt

MOSCOW_TZ = ZoneInfo("Europe/Moscow")

async def verify_access_token(
        request: Request,
        response: Response
):
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="Access token missing")

    try:
        payload = decode_jwt(
            token=access_token,
        )
        current_time = datetime.now(MOSCOW_TZ).timestamp()
        exp = payload.get("exp")

        if current_time > exp:
            raise ExpiredSignatureError

        return payload

    except ExpiredSignatureError:
        data_refresh = refresh_user_access_token(request)
        new_access_token = create_access_token(data_refresh['sub'])
        response.delete_cookie('access_token', secure=True, httponly=True, samesite="lax")
        response.set_cookie('access_token', new_access_token, secure=True, httponly=True, samesite="lax")
        payload = decode_jwt(
            token=new_access_token,
        )
        return payload

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid access_token")