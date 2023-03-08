from uuid import uuid4

import pytest
from fastapi import FastAPI, status
from fastapi_keycloak import OIDCUser
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from kafka_demo.tests.test_unit.test_db.test_crud import create_species_characteristic
from kafka_demo.schemas.enum import MaterialId
from kafka_demo.web.api.dependencies import get_current_user


class TestCatalogRoute:
    @pytest.mark.asyncio
    async def test_get_characteristics(
        self,
        dbsession: AsyncSession,
        http_client: AsyncClient,
        fastapi_app: FastAPI,
        rubble_characteristic_names: list[str],
        str_value: str,
        keycloak_user: OIDCUser,
    ) -> None:
        """
        Checks get characteristics by material endpoint.

        :param dbsession: db session.
        :param http_client: client for the kafka_demo.
        :param fastapi_app: current FastAPI application.
        :param str_value: string value.
        :param keycloak_user: keycloak user.
        """
        fastapi_app.dependency_overrides[get_current_user] = lambda: keycloak_user

        await create_species_characteristic(dbsession, str_value)
        url = fastapi_app.url_path_for(
            "get_characteristics_by_material_id",
            material_id=MaterialId.rubble.value,
        )
        response = await http_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()

    @pytest.mark.asyncio
    async def test_get_characteristic(
        self,
        dbsession: AsyncSession,
        http_client: AsyncClient,
        fastapi_app: FastAPI,
        str_value: str,
        keycloak_user: OIDCUser,
    ) -> None:
        """
        Checks get characteristic by id endpoint.

        :param dbsession: db session.
        :param http_client: client for the kafka_demo.
        :param fastapi_app: current FastAPI application.
        :param str_value: string value.
        :param keycloak_user: keycloak user.
        """
        fastapi_app.dependency_overrides[get_current_user] = lambda: keycloak_user

        characteristic_id = (await create_species_characteristic(dbsession, str_value))[
            0
        ]
        url = fastapi_app.url_path_for(
            "get_characteristic",
            characteristic_id=characteristic_id,
        )
        response = await http_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()[str_value] == str_value

    @pytest.mark.asyncio
    async def test_get_not_existing_characteristic(
        self,
        http_client: AsyncClient,
        fastapi_app: FastAPI,
        keycloak_user: OIDCUser,
    ) -> None:
        """
        Checks get not existing characteristic by id endpoint.

        :param http_client: client for the kafka_demo.
        :param fastapi_app: current FastAPI application.
        :param keycloak_user: keycloak user.
        """
        fastapi_app.dependency_overrides[get_current_user] = lambda: keycloak_user
        characteristic_id = str(uuid4())
        url = fastapi_app.url_path_for(
            "get_characteristic",
            characteristic_id=characteristic_id,
        )
        response = await http_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert (
            response.json()["message"]
            == f"Characteristic '{characteristic_id}' not found"
        )

    @pytest.mark.asyncio
    async def test_get_materials(
        self,
        dbsession: AsyncSession,
        http_client: AsyncClient,
        fastapi_app: FastAPI,
        keycloak_user: OIDCUser,
    ) -> None:
        """
        Checks get materials endpoint.

        :param dbsession: db session.
        :param http_client: client for the kafka_demo.
        :param fastapi_app: current FastAPI application.
        :param keycloak_user: keycloak user.
        """
        fastapi_app.dependency_overrides[get_current_user] = lambda: keycloak_user
        url = fastapi_app.url_path_for("get_materials")
        response = await http_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None
