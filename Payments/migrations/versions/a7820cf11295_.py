"""empty message

Revision ID: a7820cf11295
Revises: ab8f5302dc34
Create Date: 2022-10-14 17:18:22.406676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7820cf11295'
down_revision = 'ab8f5302dc34'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('paymentintent', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('paymentintent', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('paymentintent', sa.Column('succeeded', sa.Boolean(), nullable=False))
    op.add_column('paymentintent', sa.Column('customer_id', sa.String(), nullable=False))
    op.add_column('paymentintent', sa.Column('price', sa.DECIMAL(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('paymentintent', 'price')
    op.drop_column('paymentintent', 'customer_id')
    op.drop_column('paymentintent', 'succeeded')
    op.drop_column('paymentintent', 'updated_at')
    op.drop_column('paymentintent', 'created_at')
    # ### end Alembic commands ###