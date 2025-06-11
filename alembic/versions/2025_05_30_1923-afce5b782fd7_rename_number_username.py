"""rename_number_username

Revision ID: afce5b782fd7
Revises: c06619e36eb9
Create Date: 2025-05-30 19:23:28.414013

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import String

# revision identifiers, used by Alembic.
revision: str = 'afce5b782fd7'
down_revision: Union[str, None] = 'c06619e36eb9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'number', new_column_name='username',
                    existing_type=sa.String(255),
                    existing_nullable=False,
                    existing_unique=True,
                    existing_index=True)


def downgrade() -> None:
    op.alter_column('users', 'username', new_column_name='number',
                    existing_type=sa.String(255),
                    existing_nullable=False,
                    existing_unique=True,
                    existing_index=True)
