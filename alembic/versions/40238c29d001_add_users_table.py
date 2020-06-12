"""Add users table

Revision ID: 40238c29d001
Revises:
Create Date: 2020-05-26 21:18:03.691411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40238c29d001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(length=20), nullable=False),
        sa.Column('last_name', sa.String(length=20), nullable=False),
        sa.Column('email', sa.String(length=40), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade():
    op.drop_table('users')
