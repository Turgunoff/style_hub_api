"""Create initial tables

Revision ID: 512eeda9e3e1
Revises: 934d1451e84e
Create Date: 2025-02-26 14:25:32.889144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '512eeda9e3e1'
down_revision: Union[str, None] = '934d1451e84e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
