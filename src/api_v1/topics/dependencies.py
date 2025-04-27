from typing import Union

from fastapi import Request

from src.api_v1.auth.utils import decode_jwt


async def get_id_user_or_none_from_cookie(request: Request) -> Union[str, None]:
    access_token = request.cookies.get('access_token')
    if access_token:
        try:
            return decode_jwt(token=access_token).get('sub')
        except:
            return None
    return None