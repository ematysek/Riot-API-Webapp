"""user_leagues table added

Revision ID: c0be415ae939
Revises: 65318335d308
Create Date: 2018-08-30 13:40:42.853417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0be415ae939'
down_revision = '65318335d308'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_leagues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('summonerid', sa.Integer(), nullable=True),
    sa.Column('queuetype', sa.String(), nullable=True),
    sa.Column('hotstreak', sa.Boolean(), nullable=True),
    sa.Column('wins', sa.Integer(), nullable=True),
    sa.Column('losses', sa.Integer(), nullable=True),
    sa.Column('veteran', sa.Boolean(), nullable=True),
    sa.Column('playerorteamid', sa.Integer(), nullable=True),
    sa.Column('leaguename', sa.String(), nullable=True),
    sa.Column('playerorteamname', sa.String(), nullable=True),
    sa.Column('inactive', sa.Boolean(), nullable=True),
    sa.Column('rank', sa.String(), nullable=True),
    sa.Column('tier', sa.String(), nullable=True),
    sa.Column('leaguepoints', sa.Integer(), nullable=True),
    sa.Column('freshblood', sa.Boolean(), nullable=True),
    sa.Column('leagueid', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['summonerid'], ['summoners.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_leagues_summonerid'), 'user_leagues', ['summonerid'], unique=False)
    op.create_index(op.f('ix_user_matches_accountid'), 'user_matches', ['accountid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_matches_accountid'), table_name='user_matches')
    op.drop_index(op.f('ix_user_leagues_summonerid'), table_name='user_leagues')
    op.drop_table('user_leagues')
    # ### end Alembic commands ###