"""More strict structure for user model

Revision ID: a9e38220b239
Revises: ce04ecac65c5
Create Date: 2024-08-02 17:56:59.598415

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9e38220b239'
down_revision: Union[str, None] = 'ce04ecac65c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('last_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('is_active',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('is_active',
               existing_type=sa.BOOLEAN(),
               nullable=True)
        batch_op.alter_column('hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('last_name',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###
