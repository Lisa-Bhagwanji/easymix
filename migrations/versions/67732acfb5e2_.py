"""empty message

Revision ID: 67732acfb5e2
Revises: c9f4b27e6018
Create Date: 2022-06-14 08:58:45.372281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67732acfb5e2'
down_revision = 'c9f4b27e6018'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tips',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.String(length=300), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('phone', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('coops',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('breed', sa.String(length=100), nullable=False),
    sa.Column('number_of_chickens', sa.Integer(), nullable=False),
    sa.Column('date_for_next_feed', sa.DateTime(), nullable=True),
    sa.Column('next_feed_type', sa.String(length=100), nullable=True),
    sa.Column('is_grown', sa.Boolean(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recipe',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('feed', sa.String(length=100), nullable=False),
    sa.Column('number_of_days_to_feed', sa.Integer(), nullable=False),
    sa.Column('result', sa.Integer(), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('coop_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['coop_id'], ['coops.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipe')
    op.drop_table('coops')
    op.drop_table('users')
    op.drop_table('tips')
    # ### end Alembic commands ###
