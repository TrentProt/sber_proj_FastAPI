from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.core.models.base import Base

class Users(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))  # длина может варьироваться в зависимости от хеширования
    bio: Mapped[str] = mapped_column(String(255), nullable=True)
    create_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)