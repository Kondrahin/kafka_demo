import functools
from contextlib import suppress
from typing import Any, Callable

from fastapi.security import OAuth2PasswordBearer
from fastapi_keycloak import FastAPIKeycloak, OIDCUser


class FastAPIKeycloakTest(FastAPIKeycloak):
    def __init__(self, **kwargs: Any) -> None:
        with suppress(Exception):
            super().__init__(**kwargs)

    def get_current_user(self, required_roles: list[str] = None) -> Callable:
        return lambda: OIDCUser(
            sub="",
            iat=0,
            exp=0,
            email_verified=True,
        )

    @functools.cached_property
    def user_auth_scheme(self) -> OAuth2PasswordBearer:
        return OAuth2PasswordBearer(tokenUrl="")

    @property
    def admin_token(self) -> str:
        return ""
