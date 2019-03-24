"""empty message

Revision ID: 953079209802
Revises: 44d53e66aae6
Create Date: 2019-03-23 18:24:02.366085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '953079209802'
down_revision = '44d53e66aae6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('TransaksiEvent', sa.Column('bandName', sa.String(length=100), nullable=False))
    op.add_column('TransaksiEvent', sa.Column('band_id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('TransaksiEvent', 'band_id')
    op.drop_column('TransaksiEvent', 'bandName')
    # ### end Alembic commands ###