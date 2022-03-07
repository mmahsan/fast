"""add content column to posts

Revision ID: 3a81da24098a
Revises: fd2f61490302
Create Date: 2022-03-07 08:52:02.315302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a81da24098a'
down_revision = 'fd2f61490302'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
