"""empty message

Revision ID: ab8f5302dc34
Revises: a544f641439f
Create Date: 2022-10-14 14:28:57.615304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab8f5302dc34'
down_revision = 'a544f641439f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('paymentintent', sa.Column('start_date', sa.Date(), nullable=False))
    op.add_column('paymentintent', sa.Column('end_date', sa.Date(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('paymentintent', 'end_date')
    op.drop_column('paymentintent', 'start_date')
    # ### end Alembic commands ###
