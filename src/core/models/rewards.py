from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Users
from src.core.models.base import Base


class Rewards(Base):
    __tablename__ = 'rewards'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    description: Mapped[str] = mapped_column(String(50))
    image_url: Mapped[str] = mapped_column(String(255))

    user: Mapped[list['Users']] = relationship(back_populates='reward')