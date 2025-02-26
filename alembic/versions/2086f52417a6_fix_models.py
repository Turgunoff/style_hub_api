"""Fix models

Revision ID: 2086f52417a6
Revises: aa3f01ad3962
Create Date: 2025-02-26 14:33:59.899564

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2086f52417a6'
down_revision: Union[str, None] = 'aa3f01ad3962'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
