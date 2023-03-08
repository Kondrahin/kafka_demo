import uuid

import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from kafka_demo.db.repos.ticket_repo import CharacteristicRepo
from kafka_demo.tests.test_unit.test_db.test_crud import (
    create_material,
    create_species_characteristic,
)
from kafka_demo.schemas.enum import MaterialId


class TestCharacteristicRepo:
    @pytest.mark.asyncio
    async def test_get_list_characteristics_names(
        self,
        dbsession: AsyncSession,
        rubble_characteristic_names: list[str],
    ) -> None:
        """
        Checks get list characteristics names in characteristic repo.

        :param dbsession: db session.
        :param rubble_characteristic_names: sand characteristics names list.
        """

        repo = CharacteristicRepo(dbsession)
        material_list = repo._get_list_characteristics_names(MaterialId.rubble)
        assert material_list == rubble_characteristic_names

    @pytest.mark.asyncio
    async def test_get_materials(
        self,
        dbsession: AsyncSession,
        str_value: str,
    ) -> None:
        """
        Checks get materials in characteristic repo.

        :param dbsession: db session.
        :param str_value: string value.
        """

        repo = CharacteristicRepo(dbsession)
        async with dbsession.begin():
            await create_material(dbsession, str_value)
            materials_list = await repo.get_materials()
        assert materials_list[0].value == str_value

    @pytest.mark.asyncio
    async def test_get_characteristics_by_names(
        self,
        dbsession: AsyncSession,
        str_value: str,
    ) -> None:
        """
        Checks get characteristics by names in characteristic repo.

        :param dbsession: db session.
        :param str_value: string value.
        """

        repo = CharacteristicRepo(dbsession)
        async with dbsession.begin():
            await create_species_characteristic(dbsession, str_value)
            characteristics_list = await repo.get_characteristics_by_material_id(
                MaterialId.rubble,
            )
        assert characteristics_list["rubble_species"][0].value == str_value

    @pytest.mark.asyncio
    async def test_get_characteristic_by_id(
        self,
        dbsession: AsyncSession,
        str_value: str,
    ) -> None:
        """
        Checks get characteristic by id in characteristic repo.

        :param dbsession: db session.
        :param str_value: string value.
        """

        repo = CharacteristicRepo(dbsession)
        async with dbsession.begin():
            material_id = (await create_species_characteristic(dbsession, str_value))[0]
            characteristic = await repo.get_characteristic_by_id(material_id)
        assert characteristic.value == str_value

    @pytest.mark.asyncio
    async def test_get_characteristic_by_id_not_found(
        self,
        dbsession: AsyncSession,
    ) -> None:
        """
        Checks no characteristic found by id in characteristic repo.

        :param dbsession: db session.
        """

        repo = CharacteristicRepo(dbsession)
        async with dbsession.begin():
            with pytest.raises(NoResultFound):
                await repo.get_characteristic_by_id(uuid.uuid4())
