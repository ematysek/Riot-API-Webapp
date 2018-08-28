"""summoner name index

Revision ID: 65318335d308
Revises: 1b4fbccc34e7
Create Date: 2018-08-24 06:35:04.209882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65318335d308'
down_revision = '1b4fbccc34e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_summoners_name'), 'summoners', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_summoners_name'), table_name='summoners')
    # ### end Alembic commands ###