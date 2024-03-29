"""empty message

Revision ID: acaa2f0f1c25
Revises: 03f45e1b7181
Create Date: 2022-10-03 22:55:39.861618

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'acaa2f0f1c25'
down_revision = '03f45e1b7181'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(), nullable=True),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('expires_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_token_id'), 'token', ['id'], unique=False)
    op.create_index(op.f('ix_token_jti'), 'token', ['jti'], unique=True)
    op.add_column('blacklistedtoken', sa.Column('token_id', sa.Integer(), nullable=True))
    op.drop_index('ix_blacklistedtoken_jti', table_name='blacklistedtoken')
    op.create_foreign_key(None, 'blacklistedtoken', 'token', ['token_id'], ['id'])
    op.drop_column('blacklistedtoken', 'jti')
    op.drop_column('blacklistedtoken', 'expires_at')
    op.drop_column('blacklistedtoken', 'token')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blacklistedtoken', sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('blacklistedtoken', sa.Column('expires_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('blacklistedtoken', sa.Column('jti', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'blacklistedtoken', type_='foreignkey')
    op.create_index('ix_blacklistedtoken_jti', 'blacklistedtoken', ['jti'], unique=False)
    op.drop_column('blacklistedtoken', 'token_id')
    op.drop_index(op.f('ix_token_jti'), table_name='token')
    op.drop_index(op.f('ix_token_id'), table_name='token')
    op.drop_table('token')
    # ### end Alembic commands ###
