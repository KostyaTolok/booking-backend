"""empty message

Revision ID: a544f641439f
Revises: 5f4bdfbc903f
Create Date: 2022-10-14 13:32:18.086060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a544f641439f'
down_revision = '5f4bdfbc903f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('paymentintent', sa.Column('apartment_id', sa.Integer(), nullable=False))
    op.drop_column('paymentintent', 'room_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('paymentintent', sa.Column('room_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('paymentintent', 'apartment_id')
    # ### end Alembic commands ###
