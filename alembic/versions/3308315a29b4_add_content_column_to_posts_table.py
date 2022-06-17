"""Add content column to posts table

Revision ID: 3308315a29b4
Revises: 282c58acab08
Create Date: 2022-06-17 15:15:16.882890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3308315a29b4'
down_revision = '282c58acab08'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String, nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
