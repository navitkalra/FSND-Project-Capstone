"""empty message

Revision ID: 8321ee02fa02
Revises: 
Create Date: 2020-06-16 00:10:48.145677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8321ee02fa02'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('actors', sa.Column('height', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('actors', 'height')
    # ### end Alembic commands ###
