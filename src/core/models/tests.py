from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import UserAttempts
from src.core.models.base import Base

class Topics(Base):
    __tablename__ = 'topics'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(String(255))

    test: Mapped[list['TestsName']] = relationship(back_populates='topic')

class TestsName(Base):
    __tablename__ = 'tests'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    topic_id: Mapped[int] = mapped_column(Integer, ForeignKey('topics.id'), index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(String(255))
    # В секундах
    time_test: Mapped[int] = mapped_column(Integer)

    topic: Mapped['Topics'] = relationship(back_populates='test')
    question: Mapped[list['Questions']] = relationship(back_populates='test')
    user_attempt: Mapped[list['UserAttempts']] = relationship(back_populates='test')


class Questions(Base):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    test_id: Mapped[int] = mapped_column(Integer, ForeignKey('tests.id'), index=True)
    question_text: Mapped[str] = mapped_column(String(255), unique=True)

    test: Mapped['TestsName'] = relationship(back_populates='question')
    answer: Mapped[list['Answers']] = relationship(back_populates='question')


class Answers(Base):
    __tablename__ = 'answers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey('questions.id'), index=True)
    answer_text: Mapped[str] = mapped_column(String(255))
    correct: Mapped[bool] = mapped_column(Boolean, index=True)

    question: Mapped['Questions'] = relationship(back_populates='answer')

