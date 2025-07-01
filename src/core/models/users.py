from datetime import datetime
from typing import Union, TYPE_CHECKING
from sqlalchemy.sql import func
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from src.core.models.base import Base

if TYPE_CHECKING:
    from src.core.models import Topics
    from src.core.models.rewards import UserReward
    from src.core.models.tests import TestsName
    from src.core.models.cases import Cases


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255), index=True)
    create_at: Mapped[datetime] = mapped_column(default=func.now())

    profile: Mapped['Profiles'] = relationship(back_populates='user', uselist=False)
    user_attempt: Mapped[list['UserAttempts']] = relationship(back_populates='user')
    rewards: Mapped[list['UserReward']] = relationship(back_populates='user')
    user_attempt_case: Mapped[list['UserAttemptsCase']] = relationship(back_populates='user')


class Profiles(Base):
    __tablename__ = 'profiles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), unique=True, index=True)
    first_name: Mapped[Union[str, None]] = mapped_column(String(30), nullable=True)
    last_name: Mapped[Union[str, None]] = mapped_column(String(30), nullable=True)
    middle_name: Mapped[Union[str, None]] = mapped_column(String(30), nullable=True)
    bio: Mapped[Union[str, None]] = mapped_column(String(255), nullable=True)

    user: Mapped["Users"] = relationship(back_populates='profile')


class UserAttempts(Base):
    __tablename__ = 'user_attempts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id'), index=True
    )
    test_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('tests.id'), index=True
    )
    topic_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('topics.id'), index=True, nullable=True
    )
    count_correct_answer: Mapped[int] = mapped_column(Integer, index=True)
    time_execution: Mapped[int] = mapped_column(Integer, nullable=True)
    score: Mapped[int] = mapped_column(Integer, index=True)
    complete_at: Mapped[datetime] = mapped_column(default=func.now(), index=True)

    user: Mapped['Users'] = relationship(back_populates='user_attempt')
    test: Mapped['TestsName'] = relationship(back_populates='user_attempt')
    topic: Mapped['Topics'] = relationship(back_populates='user_attempts')


class UserAttemptsCase(Base):
    __tablename__ = 'user_attempts_case'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), index=True)
    case_id: Mapped[int] = mapped_column(Integer, ForeignKey('cases.id'), index=True)
    complete_at: Mapped[datetime] = mapped_column(default=func.now(), index=True)

    user: Mapped['Users'] = relationship(back_populates='user_attempt_case')
    case: Mapped['Cases'] = relationship(back_populates='user_attempts_case')