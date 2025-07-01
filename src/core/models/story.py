from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base


class Story(Base):
    __tablename__ = 'story'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(String(255))
    img_url: Mapped[str] = mapped_column(String(510), nullable=True)