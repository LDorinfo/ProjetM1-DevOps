"""empty message

Revision ID: 54a263f34c9c
Revises: 
Create Date: 2024-03-25 23:02:47.640725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54a263f34c9c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_watchlist')
    with op.batch_alter_table('watchlist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('genres', sa.String(length=255), nullable=True))
        batch_op.drop_column('genre')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('watchlist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('genre', sa.VARCHAR(length=32), nullable=True))
        batch_op.drop_column('genres')

    op.create_table('_alembic_tmp_watchlist',
    sa.Column('id', sa.VARCHAR(length=32), nullable=False),
    sa.Column('genres', sa.VARCHAR(length=255), nullable=False),
    sa.Column('media_type', sa.VARCHAR(length=32), nullable=True),
    sa.Column('user_id', sa.VARCHAR(length=32), nullable=False),
    sa.Column('film_id', sa.VARCHAR(length=32), nullable=False),
    sa.Column('title', sa.VARCHAR(length=60), nullable=True),
    sa.Column('poster_path', sa.VARCHAR(length=100), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###