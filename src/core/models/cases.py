from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base
from src.core.models.tests import SectionsTopic

if TYPE_CHECKING:
    from src.core.models.users import UserAttemptsCase


class Cases(Base):
    __tablename__ = 'cases'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    section_topic_id: Mapped[int] = mapped_column(Integer, ForeignKey('section_topic.id'), index=True, nullable=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(String(255))
    icon: Mapped[str] = mapped_column(String(255))

    user_attempts_case: Mapped[list['UserAttemptsCase']] = relationship(back_populates='case')
    section_topic: Mapped['SectionsTopic'] = relationship(back_populates='case')

