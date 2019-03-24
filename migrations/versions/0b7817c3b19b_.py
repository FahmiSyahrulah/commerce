"""empty message

Revision ID: 0b7817c3b19b
Revises: 953079209802
Create Date: 2019-03-23 18:52:46.154697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b7817c3b19b'
down_revision = '953079209802'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('TransaksiProduk', sa.Column('bandName', sa.String(length=100), nullable=False))
    op.add_column('TransaksiProduk', sa.Column('band_id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('TransaksiProduk', 'band_id')
    op.drop_column('TransaksiProduk', 'bandName')
    # ### end Alembic commands ###