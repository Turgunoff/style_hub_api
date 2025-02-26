"""Fix import path

Revision ID: aa3f01ad3962
Revises: 512eeda9e3e1
Create Date: 2025-02-26 14:26:37.839930

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa3f01ad3962'
down_revision: Union[str, None] = '512eeda9e3e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
