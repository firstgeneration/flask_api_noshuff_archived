"""Add user display_name

Revision ID: bfd7d05490b1
Revises: d3ac8ef89d39
Create Date: 2020-10-16 12:51:24.974795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfd7d05490b1'
down_revision = 'd3ac8ef89d39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'spotify_playlist_id',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
    op.add_column('users', sa.Column('display_name', sa.String(length=64), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'display_name')
    op.alter_column('posts', 'spotify_playlist_id',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)
    # ### end Alembic commands ###