"""add img_url columns and story

Revision ID: 80621955390f
Revises: e9214b8ece1d
Create Date: 2025-04-30 13:25:49.782761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80621955390f'
down_revision: Union[str, None] = 'e9214b8ece1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('section_topic', sa.Column('img_url', sa.String(length=255), nullable=True))
    op.add_column('sections_topics', sa.Column('img_url', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sections_topics', 'img_url')
    op.drop_column('section_topic', 'img_url')
    # ### end Alembic commands ###
