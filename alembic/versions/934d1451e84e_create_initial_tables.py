"""Create initial tables

Revision ID: 934d1451e84e
Revises: c1bbdeb327c9
Create Date: 2025-02-26 14:12:42.407909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '934d1451e84e'
down_revision: Union[str, None] = 'c1bbdeb327c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
