from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base

class Topics(Base):
    __tablename__ = 'topics'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(String(255))

class TestsName(Base):
    __tablename__ = 'tests'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    topic_id: Mapped[int] = mapped_column(Integer, ForeignKey('topics.id'))
    title: Mapped[int] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    score_for_reward: Mapped[float] = mapped_column(Integer)


class QuestionsAnswers(Base):
    __tablename__ = 'questions_answers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    test_id: Mapped[int] = mapped_column(Integer, ForeignKey('tests.id'))
    question_text: Mapped[str] = mapped_column(String(255), unique=True)
    correct_answer: Mapped[str] = mapped_column(String(255), unique=True)
