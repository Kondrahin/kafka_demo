from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from kafka_demo.db.dependencies import get_db_session
from kafka_demo.db.repos.ticket_repo import TicketRepo


async def get_ticket_repo(
    session: AsyncSession = Depends(get_db_session),
) -> TicketRepo:
    return TicketRepo(session)
