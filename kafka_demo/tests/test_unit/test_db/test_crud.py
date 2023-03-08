import uuid
from typing import Any

import pytest
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from kafka_demo.db.models.ticket import MaterialModel, RubbleSpeciesModel


async def create_material(dbsession: AsyncSession, str_value: str) -> Any:
    """
    Create material in db.

    :param dbsession: db session.
    :param str_value: string value.
    """

    query = insert(MaterialModel).values(**{"id": uuid.uuid4(), "value": str_value})
    res = await dbsession.execute(query)
    return res.inserted_primary_key  # type:ignore


async def create_species_characteristic(dbsession: AsyncSession, str_value: str) -> Any:
    """
    Create material in db.

    :param dbsession: db session.
    :param str_value: string value.
    """

    query = insert(RubbleSpeciesModel).values(
        **{"id": uuid.uuid4(), "value": str_value}
    )
    res = await dbsession.execute(query)
    return res.inserted_primary_key  # type:ignore


class TestCrud:
    @pytest.mark.asyncio
    async def test_crud_get(self, dbsession: AsyncSession, str_value: str) -> None:
        """
        Checks get method in crud.

        :param dbsession: db session.
        :param str_value: string value.
        """

        async with dbsession.begin():
            material_id = (await create_material(dbsession, str_value))[0]
            result = await MaterialModel.get(dbsession, material_id)
            assert result.value == str_value

    @pytest.mark.asyncio
    async def test_crud_all(self, dbsession: AsyncSession, str_value: str) -> None:
        """
        Checks get method in crud.

        :param dbsession: db session.
        :param str_value: string value.
        """

        async with dbsession.begin():
            await create_material(dbsession, str_value)
            result = await MaterialModel.all(dbsession)
            assert len(result) == 1
            assert result[0].value == str_value
