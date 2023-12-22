"""create ost table

Revision ID: 89b5c0d8fc8a
Revises: 
Create Date: 2023-12-22 10:28:20.276770

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89b5c0d8fc8a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True)
                    ,sa.Column('title',sa.String(),nullable=False))
    


def downgrade() -> None:
    
    op.drop_table("posts")
    pass
