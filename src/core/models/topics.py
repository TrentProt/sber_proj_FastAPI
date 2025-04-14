from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base

class Topics(Base):
    __tablename__ = 'topics'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(String)


