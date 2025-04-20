from datetime import datetime

from fastapi import HTTPException, Request

from src.auth.utils import decode_jwt


async def verify_access_token(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token missing")
    try:
        payload = decode_jwt(
            token=access_token,
        )
        current_time = datetime.utcnow().timestamp()
        exp = payload.get("exp")
        if current_time > exp:
            raise HTTPException(status_code=401, detail="Token expired")
        return payload
    except:
        raise HTTPException(status_code=401, detail=f"Invalid access_token")


async def refresh_user_access_token(request: Request):
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    try:
        payload = decode_jwt(token=refresh_token)
        current_time = datetime.utcnow().timestamp()
        exp = payload.get("exp")
        if current_time > exp:
            raise HTTPException(status_code=401, detail="Token expired")
        return payload
    except:
        raise HTTPException(status_code=401, detail=f"Invalid refresh_token")
