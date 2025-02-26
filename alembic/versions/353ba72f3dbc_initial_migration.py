"""Initial migration

Revision ID: 353ba72f3dbc
Revises: 63dace2974a0
Create Date: 2025-02-26 17:24:27.531031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '353ba72f3dbc'
down_revision: Union[str, None] = '63dace2974a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
