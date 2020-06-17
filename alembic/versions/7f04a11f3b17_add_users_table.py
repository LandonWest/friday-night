"""Add users table

Revision ID: 7f04a11f3b17
Revises:
Create Date: 2020-06-15 22:27:16.013090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f04a11f3b17'
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
        sa.Column(
            'media_entry_id',
            sa.Integer,
            sa.ForeignKey("media_entries.id"),
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade():
    op.drop_table('users')
