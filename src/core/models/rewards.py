from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base


class Rewards(Base):
    __tablename__ = 'rewards'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    test_id: Mapped[int] = mapped_column(Integer, ForeignKey('tests.id'))
    name: Mapped[str] = mapped_column(String(32), unique=True)
    description: Mapped[str] = mapped_column(String(50))
    image_url: Mapped[str] = mapped_column(String(255))
