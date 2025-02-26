"""Create initial tables

Revision ID: 63dace2974a0
Revises: 2086f52417a6
Create Date: 2025-02-26 14:34:39.760368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63dace2974a0'
down_revision: Union[str, None] = '2086f52417a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
