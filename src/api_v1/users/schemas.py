from typing import Union

from pydantic import BaseModel


class CreateProfile(BaseModel):
    first_name: str
    last_name: str
    middle_name: Union[str, None] = None


class UpdateProfile(CreateProfile):
    bio: Union[str, None] = None


class GetProfile(UpdateProfile):
    id: int
    user_id: int
