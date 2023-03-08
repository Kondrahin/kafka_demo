from uuid import UUID, uuid4

import pytest
from fastapi_keycloak import OIDCUser


@pytest.fixture
def str_value() -> str:
    return "value"


@pytest.fixture
def rubble_characteristic_names() -> list[str]:
    return [
        "rubble_species",
        "fraction",
        "leshchadnost",
        "strength",
        "frost_resistance",
        "radioactivity",
        "standard",
        "bulk_density",
    ]


@pytest.fixture
def user_id() -> UUID:
    return uuid4()


@pytest.fixture
def keycloak_user(user_id: UUID) -> OIDCUser:
    return OIDCUser(sub=str(user_id), iat=1, exp=100, email_verified=True)
