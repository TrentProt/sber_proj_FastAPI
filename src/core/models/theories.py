from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base

if TYPE_CHECKING:
    from src.core.models.tests import SectionsTopic


class TheoriesTable(Base):
    __tablename__ = 'theories'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    section_topic_id: Mapped[int] = mapped_column(Integer, ForeignKey('section_topic.id'))
    book: Mapped[str] = mapped_column(String(255))
    link: Mapped[str] = mapped_column(String(255))

    section_topic: Mapped['SectionsTopic'] = relationship(back_populates='theories')