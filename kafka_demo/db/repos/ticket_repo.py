from contextlib import suppress
from typing import Any
from uuid import UUID

from asyncstdlib.functools import lru_cache
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from kafka_demo.db.models.ticket import TicketModel
from kafka_demo.web.api.kafka.schema import TicketSchema, TicketCreateSchema


class TicketRepo:
    def __init__(self, session: AsyncSession):
        """Initialize repo with session."""
        self._session = session

    async def create(self, model_data: TicketCreateSchema):
        return await TicketModel.create(self._session, model_data.dict())

    async def get_ticket_by_id(
        self,
        ticket_id: UUID,
    ) -> TicketSchema:
        """Get ticket by id"""
        ticket = await TicketModel.get(self._session, ticket_id)

        return TicketSchema.from_orm(ticket)

    async def mark_as_completed(self, ticket_id: UUID):
        await TicketModel.update(
            session=self._session,
            pkey_val=ticket_id,
            model_data={"is_completed": True}
        )
