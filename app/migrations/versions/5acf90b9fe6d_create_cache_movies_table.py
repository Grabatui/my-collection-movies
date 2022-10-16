"""create_cache_movies_table

Revision ID: 5acf90b9fe6d
Revises: 
Create Date: 2022-10-15 23:35:19.235575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5acf90b9fe6d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'cache_movies',
        sa.Column('id', sa.Integer),
        sa.Column('supplier', sa.String, nullable=False),
        sa.Column('external_id', sa.String, nullable=False),
        sa.Column('data', sa.Text, nullable=False),
        sa.Column('inserted_at', sa.DateTime, nullable=False),

        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('cache_movies')
