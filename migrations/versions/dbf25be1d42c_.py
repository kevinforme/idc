"""empty message

Revision ID: dbf25be1d42c
Revises: 23c542edc763
Create Date: 2018-05-03 14:00:34.034981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbf25be1d42c'
down_revision = '23c542edc763'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notices', sa.Column('timestamp', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notices', 'timestamp')
    # ### end Alembic commands ###
