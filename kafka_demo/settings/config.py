from typing import Dict, Type

from kafka_demo.settings.environments.base import AppEnvTypes, BaseAppSettings, Settings
from kafka_demo.settings.environments.dev import DevSettings

environments: Dict[str, Type[Settings]] = {
    AppEnvTypes.DEV: DevSettings,
}

settings = DevSettings()
