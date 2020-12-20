"""book_img_src

Revision ID: bc66587fd935
Revises: 1c6f4de60151
Create Date: 2020-12-31 06:34:33.830761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc66587fd935'
down_revision = '1c6f4de60151'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Diary', sa.Column('book_img_src', sa.String(length=1024), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Diary', 'book_img_src')
    # ### end Alembic commands ###
