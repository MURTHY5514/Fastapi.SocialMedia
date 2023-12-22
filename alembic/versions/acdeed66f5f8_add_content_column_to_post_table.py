"""add content column to post table

Revision ID: acdeed66f5f8
Revises: 89b5c0d8fc8a
Create Date: 2023-12-22 10:59:32.499400

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acdeed66f5f8'
down_revision: Union[str, None] = '89b5c0d8fc8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass