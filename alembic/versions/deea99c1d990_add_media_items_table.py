"""Add media_items table

Revision ID: deea99c1d990
Revises: b80a02cbead2
Create Date: 2020-06-15 23:13:05.366190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'deea99c1d990'
down_revision = 'b80a02cbead2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'media_items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(80), nullable=False, unique=True),
        sa.Column('rated', sa.String(8)),
        sa.Column('release_date', sa.Date),
        sa.Column('runtime', sa.String(8)),
        sa.Column('genre', sa.String(80)),
        sa.Column('director', sa.String(20)),
        sa.Column('cast', sa.String(120)),
        sa.Column('plot', sa.Text),
        sa.Column('awards', sa.String(120)),
        sa.Column('poster', sa.String(180)),
        sa.Column('imdb_rating', sa.Float),
        sa.Column('rotten_tomatoes_rating', sa.String(20)),
        sa.Column('imdb_id', sa.String(20)),
        sa.Column('media_type', sa.String(20)),
        sa.Column('total_seasons', sa.Integer),
        sa.Column('box_office_earnings', sa.Integer),
        sa.Column('production_studio', sa.String(40)),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('media_items')
