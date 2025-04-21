from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from src.core.models.base import Base

if TYPE_CHECKING:
    from src.core.models.users import Users
    from src.core.models.tests import Topics

class Rewards(Base):
    __tablename__ = 'rewards'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    description: Mapped[str] = mapped_column(String(50))
    image_url: Mapped[str] = mapped_column(String(255))

    user_reward: Mapped[list['UserReward']] = relationship(back_populates='reward')


class UserReward(Base):
    __tablename__ = 'user_reward'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    topic_id: Mapped[int] = mapped_column(Integer, ForeignKey('topics.id'))
    reward_id: Mapped[int] = mapped_column(Integer, ForeignKey('rewards.id'))

    user: Mapped['Users'] = relationship(back_populates='rewards')
    topic: Mapped['Topics'] = relationship(back_populates='user_reward')
    reward: Mapped['Rewards'] = relationship(back_populates='user_reward')
