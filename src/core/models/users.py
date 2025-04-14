from datetime import datetime
from typing import Union

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.core.models.base import Base

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    create_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class Profile(Base):
    __tablename__ = 'profiles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    first_name: Mapped[Union[str, None]] = mapped_column(String(30), nullable=True)
    last_name: Mapped[Union[str, None]] = mapped_column(String(30), nullable=True)
    middle_name: Mapped[Union[str, None]] = mapped_column(String(30), nullable=True)
    bio: Mapped[Union[str, None]] = mapped_column(String(255), nullable=True)

