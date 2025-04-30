from datetime import datetime, time
from typing import Union, TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey, Time, Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base


if TYPE_CHECKING:
    from src.core.models.rewards import UserReward
    from src.core.models.tests import TestsName


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String(12), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255), index=True)
    create_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    profile: Mapped['Profiles'] = relationship(back_populates='user', uselist=False)
    user_attempt: Mapped[list['UserAttempts']] = relationship(back_populates='user')
    rewards: Mapped[list['UserReward']] = relationship(back_populates='user')


class Profiles(Base):
    __tablename__ = 'profiles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), unique=True)
    first_name: Mapped[Union[str, None]] = mapped_column(String(30), nullable=True)
    last_name: Mapped[Union[str, None]] = mapped_column(String(30), nullable=True)
    middle_name: Mapped[Union[str, None]] = mapped_column(String(30), nullable=True)
    bio: Mapped[Union[str, None]] = mapped_column(String(255), nullable=True)

    user: Mapped["Users"] = relationship(back_populates='profile')


class UserAttempts(Base):
    __tablename__ = 'user_attempts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), index=True)
    test_id: Mapped[int] = mapped_column(Integer, ForeignKey('tests.id'), index=True)
    count_correct_answer: Mapped[int] = mapped_column(Integer)
    time_execution: Mapped[time] = mapped_column(Time)
    score: Mapped[int] = mapped_column(Integer)
    complete_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)

    __table_args__ = (
        UniqueConstraint('user_id', 'test_id'),
    )

    user: Mapped['Users'] = relationship(back_populates='user_attempt')
    test: Mapped['TestsName'] = relationship(back_populates='user_attempt')



