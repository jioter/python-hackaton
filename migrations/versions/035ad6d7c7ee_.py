"""empty message

Revision ID: 035ad6d7c7ee
Revises: 81cc15773984
Create Date: 2019-07-06 14:42:56.064628

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '035ad6d7c7ee'
down_revision = '81cc15773984'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('from_number', sa.Integer(), nullable=False),
    sa.Column('to_number', sa.Integer(), nullable=False),
    sa.Column('attempts', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_completed', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('game_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('retries', sa.Integer(), nullable=False),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('date_start', sa.DateTime(), nullable=True),
    sa.Column('date_finish', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.alter_column('user', 'login',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('user', 'create_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('create_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'login',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('user', 'date_created')
    op.drop_table('game_results')
    op.drop_table('game')
    # ### end Alembic commands ###
