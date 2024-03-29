"""empty message

Revision ID: 5f4bdfbc903f
Revises:
Create Date: 2022-10-12 19:04:26.199788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f4bdfbc903f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('paymentintent',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('payment_intent_id', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_paymentintent_id'), 'paymentintent', ['id'], unique=False)
    op.create_index(op.f('ix_paymentintent_payment_intent_id'), 'paymentintent', ['payment_intent_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_paymentintent_payment_intent_id'), table_name='paymentintent')
    op.drop_index(op.f('ix_paymentintent_id'), table_name='paymentintent')
    op.drop_table('paymentintent')
    # ### end Alembic commands ###
