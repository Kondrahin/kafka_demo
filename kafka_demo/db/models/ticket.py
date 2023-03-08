import uuid
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from kafka_demo.db.base import Base
from kafka_demo.db.crud import CRUDMixin


class TicketModel(Base, CRUDMixin):
    """Base characteristic database model."""

    __tablename__ = "ticket"

    id: UUID = sa.Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        unique=True,
        default=uuid.uuid4
    )

    title: str = sa.Column(sa.String, nullable=False)
    is_completed: bool = sa.Column(sa.Boolean, default=False, nullable=False)
