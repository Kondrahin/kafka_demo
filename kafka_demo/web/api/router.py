from fastapi.routing import APIRouter

from kafka_demo.web.api import docs, monitoring, kafka

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(kafka.router)
