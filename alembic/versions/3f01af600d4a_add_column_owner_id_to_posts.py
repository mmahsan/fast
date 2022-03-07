"""add column owner_id to posts

Revision ID: 3f01af600d4a
Revises: c2e6786cc535
Create Date: 2022-03-07 09:20:29.129559

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f01af600d4a'
down_revision = 'c2e6786cc535'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
    nullable=False, server_default=sa.text('NOW()')))
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.create_foreign_key('posts_users_fkey', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts', 'owner_id')
    op.drop_column('posts', 'created_at')
    pass
