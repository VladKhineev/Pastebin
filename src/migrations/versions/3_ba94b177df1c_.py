"""empty message

Revision ID: ba94b177df1c
Revises: 6ace96d7dfdc
Create Date: 2024-10-24 15:09:49.709639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba94b177df1c'
down_revision: Union[str, None] = '6ace96d7dfdc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('like', sa.Integer(), server_default=sa.text("0"), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'like')
    # ### end Alembic commands ###
