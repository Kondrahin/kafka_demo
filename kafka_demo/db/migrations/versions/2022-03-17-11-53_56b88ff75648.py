"""Ticket model

Revision ID: 56b88ff75648
Revises: 819cbf6e030b
Create Date: 2022-03-17 11:53:39.436216

"""
import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
from kafka_demo.settings import settings

revision = "56b88ff75648"
down_revision = "819cbf6e030b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ticket",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, default=uuid.uuid4),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("is_completed", sa.Boolean(), default=False ,nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("ticket")
    # ### end Alembic commands ###