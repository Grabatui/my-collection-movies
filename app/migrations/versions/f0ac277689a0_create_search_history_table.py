"""create_search_history_table

Revision ID: f0ac277689a0
Revises: 5acf90b9fe6d
Create Date: 2022-10-18 11:58:49.420829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0ac277689a0'
down_revision = '5acf90b9fe6d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'search_history',
        sa.Column('id', sa.Integer),
        sa.Column('query', sa.String, nullable=False),
        sa.Column('inserted_at', sa.DateTime, nullable=False),

        sa.PrimaryKeyConstraint('id')
    )

    op.add_column(
        'cache_movies',
        sa.Column('search_history_id', sa.Integer, sa.ForeignKey('search_history.id'))
    )

    op.rename_table('cache_movies', 'search_movies')


def downgrade() -> None:
    op.rename_table('search_movies', 'cache_movies')
    op.drop_column('cache_movies', 'search_history_id')
    op.drop_table('search_history')

