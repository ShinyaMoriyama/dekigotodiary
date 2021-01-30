"""stripe

Revision ID: 0f9f9eada768
Revises: c5add6c0425e
Create Date: 2021-01-24 15:07:37.876098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f9f9eada768'
down_revision = 'c5add6c0425e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User', sa.Column('stripe_customer', sa.String(length=64), nullable=True))
    op.add_column('User', sa.Column('stripe_status', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('User', 'stripe_status')
    op.drop_column('User', 'stripe_customer')
    # ### end Alembic commands ###