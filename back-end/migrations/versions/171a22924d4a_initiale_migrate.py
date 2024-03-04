"""Initiale migrate

Revision ID: 171a22924d4a
Revises: 
Create Date: 2023-12-29 11:20:23.657260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '171a22924d4a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.create_unique_constraint('comments_id', ['id'])
        batch_op.drop_column('likes')

    with op.batch_alter_table('evenement', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.String(length=32), nullable=False))
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=64),
               nullable=True)
        batch_op.create_foreign_key('fk_evenement_user_id', 'users', ['user_id'], ['id'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('isconnected')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('isconnected', sa.BOOLEAN(), nullable=True))

    with op.batch_alter_table('evenement', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('description',
               existing_type=sa.String(length=64),
               type_=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
        batch_op.drop_column('user_id')

    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('likes', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###