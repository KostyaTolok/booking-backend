"""empty message

Revision ID: 5596f3ee83c6
Revises: f3a656b6e99b
Create Date: 2022-11-19 21:46:37.185297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5596f3ee83c6'
down_revision = 'f3a656b6e99b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookingpayment', sa.Column('client_secret', sa.String(), nullable=False))
    op.create_index(op.f('ix_bookingpayment_client_secret'), 'bookingpayment', ['client_secret'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_bookingpayment_client_secret'), table_name='bookingpayment')
    op.drop_column('bookingpayment', 'client_secret')
    # ### end Alembic commands ###
