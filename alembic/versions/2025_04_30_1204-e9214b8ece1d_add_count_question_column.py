"""add count_question column

Revision ID: e9214b8ece1d
Revises: 70ddef2e3d21
Create Date: 2025-04-30 12:04:16.859082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9214b8ece1d'
down_revision: Union[str, None] = '70ddef2e3d21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tests', sa.Column('count_question', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tests', 'count_question')
    # ### end Alembic commands ###
