import json
import os

import boto3

from src.cloudhive.logger import Logger

logger = Logger.get_logger(name=f"cloudhive{__file__}")
logger.set_level("debug")


def json_type(data: str):
    if "=" in data:
        return json.loads(data.replace("=", ":").replace("'", "\""))
    return None


ENV_VAR_MAPPING = {
    "DEBUG": {"cast_type": bool, "default": True},
    "FORCE_EMAIL": {"cast_type": bool, "default": False},
    "FORCE_SCP": {"cast_type": bool, "default": False},
    "RETENTION": {"cast_type": int, "default": 1},
    "DB_TABLE_NAME": {"cast_type": str, "default": ""},
    "ENV": {"cast_type": str, "default": ""},
    "AWS_LAMBDA_FUNCTION_NAME": {"cast_type": str, "default": "Default setting"},
    "DB_ROTATION_PERIOD": {"cast_type": int, "default": 7},
    "BUCKET_MAPPING": {"cast_type": json_type, "default": []}
}


class EnvConfig:
    def __init__(self, mapping):
        self._mapping: dict[str, dict] = mapping

    def cast(self, item, value):
        cast_type = self._mapping[item]['cast_type']
        if cast_type is bool:
            if isinstance(value, str):
                return str(value).lower() in ("1", "true", "yes", "on")
        try:
            return cast_type(value)
        except (ValueError, TypeError):
            logger.debug(f"Using the default value for key '{item}' with type of {type(item)}")
            return self._mapping[item]['default']
        except json.JSONDecodeError:
            logger.error("Can't able to decode the variable")
            return []

    def __getitem__(self, item):
        value = os.environ.get(item, self._mapping[item]['default'])
        return self.cast(item, value)

    def __getattr__(self, item):
        if item in self._mapping:
            return self.__getitem__(item)
        raise AttributeError(f"{self.__class__.__name__} has not attribute '{item}'")

    def __repr__(self):
        return f"<{self.__class__.__name__} key={list(self._mapping.keys())}>"

"""
>>> env = EnvConfig(ENV_VAR_MAPPING)
"""