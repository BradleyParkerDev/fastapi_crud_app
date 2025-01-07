"""Initial Migration

Revision ID: 8cad8ba13268
Revises: 
Create Date: 2025-01-03 12:19:29.538787

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cad8ba13268'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('user_image', sa.String(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email_address', sa.String(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('last_updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email_address'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('user_sessions',
    sa.Column('session_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('expiration_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('session_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_sessions')
    op.drop_table('users')
    # ### end Alembic commands ###
