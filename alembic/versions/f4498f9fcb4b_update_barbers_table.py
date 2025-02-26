"""Update barbers table

Revision ID: f4498f9fcb4b
Revises: cfb90146efd6
Create Date: 2025-02-26 17:42:51.887257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4498f9fcb4b'
down_revision: Union[str, None] = 'cfb90146efd6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
