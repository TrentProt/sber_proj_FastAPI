from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base
from src.core.models.rewards import UserReward

if TYPE_CHECKING:
    from src.core.models.users import UserAttempts
    from src.core.models.rewards import UserReward
    from src.core.models.cases import Cases
    from src.core.models.theories import TheoriesTable

class Topics(Base):
    __tablename__ = 'topics'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(String(255))

    user_reward: Mapped[list['UserReward']] = relationship(back_populates='topic')
    section_topic: Mapped[list['SectionsTopic']] = relationship(back_populates='topic')
    cases: Mapped[list['Cases']] = relationship(back_populates='topic')
    user_attempts: Mapped[list['UserAttempts']] = relationship(back_populates='topic')


class SectionsTopic(Base):
    __tablename__ = 'section_topic'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    topic_id: Mapped[int] = mapped_column(Integer, ForeignKey('topics.id'), index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    img_url: Mapped[str] = mapped_column(String(255), nullable=True)

    topic: Mapped['Topics'] = relationship(back_populates='section_topic')
    test: Mapped[list['TestsName']] = relationship(back_populates='section_topic')
    case: Mapped[list['Cases']] = relationship(back_populates='section_topic')
    theories: Mapped[list['TheoriesTable']] = relationship(back_populates='section_topic')


class TestsName(Base):
    __tablename__ = 'tests'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    section_topic_id: Mapped[int] = mapped_column(Integer, ForeignKey('section_topic.id'), index=True)
    type_test: Mapped[str] = mapped_column(String(20), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    count_question: Mapped[int] = mapped_column(Integer, nullable=True)
    # В секундах
    time_test: Mapped[int] = mapped_column(Integer)

    questions: Mapped[list['Questions']] = relationship(back_populates='test')
    user_attempt: Mapped[list['UserAttempts']] = relationship(back_populates='test')
    section_topic: Mapped['SectionsTopic'] = relationship(back_populates='test')


class Questions(Base):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    test_id: Mapped[int] = mapped_column(Integer, ForeignKey('tests.id'), index=True)
    question_text: Mapped[str] = mapped_column(String(255), unique=True)

    test: Mapped['TestsName'] = relationship(back_populates='questions')
    answers: Mapped[list['Answers']] = relationship(back_populates='question')


class Answers(Base):
    __tablename__ = 'answers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey('questions.id'), index=True)
    answer_text: Mapped[str] = mapped_column(String(255))
    correct: Mapped[bool] = mapped_column(Boolean, index=True)

    question: Mapped['Questions'] = relationship(back_populates='answers')


class Theories(Base):
    __tablename__ = 'theories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
