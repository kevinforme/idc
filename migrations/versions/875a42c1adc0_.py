"""empty message

Revision ID: 875a42c1adc0
Revises: 0051f9a25dd2
Create Date: 2018-05-03 15:32:21.515368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '875a42c1adc0'
down_revision = '0051f9a25dd2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('author_id', sa.Integer(), nullable=True))
    op.add_column('events', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_foreign_key(None, 'events', 'users', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.drop_column('events', 'timestamp')
    op.drop_column('events', 'author_id')
    # ### end Alembic commands ###
