"""Add Hashtags

Revision ID: f3b2343077d3
Revises: bfd7d05490b1
Create Date: 2020-10-19 21:41:49.461853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3b2343077d3'
down_revision = 'bfd7d05490b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hashtags',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hashtags')
    # ### end Alembic commands ###
