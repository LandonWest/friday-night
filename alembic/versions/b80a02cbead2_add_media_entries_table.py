"""Add media_entries table

Revision ID: b80a02cbead2
Revises: 7f04a11f3b17
Create Date: 2020-06-15 23:05:22.111819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b80a02cbead2'
down_revision = '7f04a11f3b17'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'media_entries',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('title', sa.String(length=40), nullable=False),
        sa.Column('watched', sa.Boolean, default=False),
        sa.Column('watched_date', sa.Date),
        sa.Column('user_rating', sa.Float),
        sa.Column(
            'media_item_id',
            sa.Integer,
            sa.ForeignKey("media_items.id"),
            nullable=False
        ),
        sa.Column(
            'user_id',
            sa.Integer,
            sa.ForeignKey("users.id"),
            nullable=False
        ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('media_entries')
