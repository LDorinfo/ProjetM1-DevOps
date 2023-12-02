"""changement table watchlist

Revision ID: 1cf11eb472ab
Revises: d31fd2849e0b
Create Date: 2023-12-02 11:59:23.610940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cf11eb472ab'
down_revision = 'd31fd2849e0b'
branch_labels = None
depends_on = None


def upgrade():
    # Ajouter les colonnes à la table watchlist
    with op.batch_alter_table('watchlist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=60)))
        batch_op.add_column(sa.Column('poster_path', sa.String(length=100)))

def downgrade():
    # Supprimer les colonnes de la table watchlist
    with op.batch_alter_table('watchlist', schema=None) as batch_op:
        batch_op.drop_column('poster_path')
        batch_op.drop_column('title')
