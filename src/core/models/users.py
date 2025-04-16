from datetime import datetime
from typing import Union

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.models.base import Base

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String(12), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    create_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    profile: Mapped['Profile'] = relationship(back_populates='user')


class Profile(Base):
    __tablename__ = 'profiles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    first_name: Mapped[Union[str, None]] = mapped_column(String(30), nullable=True)
    last_name: Mapped[Union[str, None]] = mapped_column(String(30), nullable=True)
    middle_name: Mapped[Union[str, None]] = mapped_column(String(30), nullable=True)
    bio: Mapped[Union[str, None]] = mapped_column(String(255), nullable=True)

    user: Mapped["Users"] = relationship(back_populates='profile')

class UserRewards(Base):
    __tablename__ = 'user_rewards'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    reward_id: Mapped[int] = mapped_column(Integer, ForeignKey('rewards.id'))
    attempt_id: Mapped[int] = mapped_column(Integer, ForeignKey('test_attempts.id'))
    awarded_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # user: Mapped[]