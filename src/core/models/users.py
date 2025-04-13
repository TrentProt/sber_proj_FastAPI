from datetime import datetime
from typing import Union

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.core.models.base import Base

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    bio: Mapped[Union[str, None]] = mapped_column(String(255), nullable=True)
    create_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)