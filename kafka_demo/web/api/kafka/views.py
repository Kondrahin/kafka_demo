import asyncio
from uuid import UUID

from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends

from kafka_demo.db.repos.ticket_repo import TicketRepo
# from kafka_demo.services.kafka.consumer import consume
from kafka_demo.services.kafka.dependencies import get_kafka_producer
from kafka_demo.web.api.dependencies import get_ticket_repo
from kafka_demo.web.api.kafka.schema import TicketCreateSchema, TicketSchema
# from kafka_demo.web.application import app

router = APIRouter()


@router.post("/")
async def send_kafka_message(
    ticket_to_create: TicketCreateSchema,
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
    ticket_repo: TicketRepo = Depends(get_ticket_repo)
) -> dict[str, UUID]:
    """
    Sends message to kafka.

    :param producer: kafka's producer.
    :param ticket_to_create: message to publish.
    :param ticket_repo: ticket repo.
    """
    ticket_id = await ticket_repo.create(ticket_to_create)
    await producer.send("demo", str(ticket_id).encode())
    return {"ticket_id": ticket_id}


@router.get("/")
async def get_ticket(
    ticket_id: UUID,
    ticket_repo: TicketRepo = Depends(get_ticket_repo)
) -> TicketSchema:
    """
    Get ticket.

    :param ticket_id: ticket id.
    :param ticket_repo: ticket repo.
    """
    return await ticket_repo.get_ticket_by_id(ticket_id)
