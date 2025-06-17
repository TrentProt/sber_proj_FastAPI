"""remove type column from section_topic table

Revision ID: e5e15fab6930
Revises: fed60cea270c
Create Date: 2025-06-15 18:12:33.617650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5e15fab6930'
down_revision: Union[str, None] = 'fed60cea270c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('section_topic', 'type')


def downgrade() -> None:
    op.add_column('section_topic',
                 sa.Column('type', sa.String(length=255), nullable=True))
