from datetime import datetime

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base

class TestAttempts(Base):
    __tablename__ = 'test_attempts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    test_id: Mapped[int] = mapped_column(Integer, ForeignKey('tests.id'))
    count_correct_answer: Mapped[int] = mapped_column(Integer)
    total_questions: Mapped[int] = mapped_column(Integer)
    complete_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)