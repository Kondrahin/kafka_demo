import httpx
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.testclient import TestClient

from kafka_demo.db.dependencies import get_db_session
from kafka_demo.web.application import get_app


@pytest.fixture(autouse=True)
async def http_client(fastapi_app: FastAPI) -> httpx.AsyncClient:
    async with LifespanManager(fastapi_app):
        async with httpx.AsyncClient(
            base_url="http://testserver",
            app=fastapi_app,
        ) as fastapi_app_client:
            yield fastapi_app_client


@pytest.fixture()
def fastapi_app(
    dbsession: AsyncSession,
) -> FastAPI:
    """
    Fixture for creating FastAPI kafka_demo.

    :return: fastapi kafka_demo with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_db_session] = lambda: dbsession

    return application


@pytest.fixture(scope="function")
def client(
    fastapi_app: FastAPI,
) -> TestClient:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :return: client for the kafka_demo.
    """
    return TestClient(app=fastapi_app)
