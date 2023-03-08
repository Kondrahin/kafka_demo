import asyncio
from uuid import UUID

from aiokafka import AIOKafkaConsumer

from fastapi import FastAPI

from kafka_demo.db.repos.ticket_repo import TicketRepo

# env variables
KAFKA_TOPIC = "demo"
KAFKA_CONSUMER_GROUP = "group"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9093"


async def consume(app: FastAPI):
    session = app.state.db_session_factory()

    ticket_repo = TicketRepo(session)
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_CONSUMER_GROUP,
        heartbeat_interval_ms=10000000
    )
    # get cluster layout and join group KAFKA_CONSUMER_GROUP
    await consumer.start()
    try:
        # consume messages
        async for msg in consumer:
            await asyncio.sleep(6)
            await ticket_repo.mark_as_completed(UUID(msg.value.decode("utf-8")))
            await session.commit()
            print(f"Consumed msg: {msg}")
    finally:
        # will leave consumer group; perform autocommit if enabled.
        await consumer.stop()
