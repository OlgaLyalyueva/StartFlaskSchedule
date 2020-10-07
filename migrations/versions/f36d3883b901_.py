"""empty message

Revision ID: f36d3883b901
Revises: fb2afb8aec01
Create Date: 2020-10-06 09:31:13.536886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f36d3883b901'
down_revision = 'fb2afb8aec01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notes',
    sa.Column('note_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=False),
    sa.Column('date_time', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('note_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notes')
    # ### end Alembic commands ###
