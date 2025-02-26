"""Add barbers table

Revision ID: cfb90146efd6
Revises: 353ba72f3dbc
Create Date: 2025-02-26 17:33:55.342014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfb90146efd6'
down_revision: Union[str, None] = '353ba72f3dbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
