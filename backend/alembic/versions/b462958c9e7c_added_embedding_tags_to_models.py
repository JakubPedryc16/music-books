"""Added embedding_tags to models

Revision ID: b462958c9e7c
Revises: f810559e594d
Create Date: 2025-07-26 18:14:21.130736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b462958c9e7c'
down_revision: Union[str, Sequence[str], None] = 'f810559e594d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('embedding_tags', sa.JSON(), nullable=True))
    op.add_column('music', sa.Column('embedding_tags', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('music', 'embedding_tags')
    op.drop_column('books', 'embedding_tags')
    # ### end Alembic commands ###
