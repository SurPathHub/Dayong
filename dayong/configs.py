# pylint: disable=R0913,R0903
"""
dayong.configs
~~~~~~~~~~~~~~

Initial setup and configuration logic.
"""
import json
import os
from typing import Any, Dict, Union
from warnings import warn

from pydantic import BaseModel

from dayong.settings import CONFIG_FILE
from dayong.utils import format_db_url

VALID_CONFIG = {
    "guild_id": int,
    "bot_prefix": str,
    "embeddings": {
        "new_member_greetings": {
            "readme_channel_id": int,
            "description": str,
            "color": int,
            "greetings_field": {
                "0": {
                    "name": str,
                    "value": str
                },
                "1": {
                    "name": str,
                    "value": str
                },
                "2": {
                    "name": str,
                    "value": str
                },
                "3": {
                    "name": str,
                    "value": str
                },
                "4": {
                    "name": str,
                    "value": str
                },
                "5": {
                    "name": str,
                    "value": str
                }
            }
        },
        "anonymous_message": {
            "title": str,
            "color": int
        }
    }
}


class DayongConfig(BaseModel):
    """Data model for Dayong's configuration."""

    bot_prefix: str
    bot_token: str
    database_uri: str
    embeddings: dict[str, Union[str, dict[str, Any]]]
    guild_id: int

    @classmethod
    def load(
        cls,
        bot_prefix: str,
        bot_token: str,
        database_uri: str,
        embeddings: dict[str, Union[str, dict[str, Any]]],
        guild_id: int,
    ) -> "DayongConfig":
        """Construct an instance of `dayong.configs.DayongConfig`.

        Returns:
            An instance of `dayong.configs.DayongConfig`.
        """
        return cls(
            bot_prefix=bot_prefix,
            bot_token=bot_token,
            database_uri=database_uri,
            guild_id=guild_id,
            embeddings=embeddings,
        )


class DayongConfigLoader:
    """Configuration loader for Dayong."""

    def __init__(self) -> None:
        self.load_cfg()
        self.load_env()

    def load_cfg(self) -> None:
        """Load comments, flags, settings, and paths from config file."""
        with open(CONFIG_FILE, encoding="utf-8") as cfp:
            config = dict(json.load(cfp))
            self.validate_cfg(config, VALID_CONFIG)
        self.bot_prefix = config["bot_prefix"]
        self.guild_id = config["guild_id"]
        self.embeddings = config["embeddings"]

    def load_env(self) -> None:
        """Load environment variables."""
        self.bot_token = os.environ["BOT_TOKEN"]
        self.database_uri = format_db_url(os.environ["DATABASE_URL"])

    @staticmethod
    def load() -> DayongConfig:
        """Load configs into `dayong.configs.DayongConfig`.

        Returns:
            DayongConfig: An instance of `dayong.configs.DayongConfig`.
        """
        loader = DayongConfigLoader().__dict__
        return DayongConfig.load(*tuple(loader[key] for key in sorted(loader.keys())))

    def validate_cfg(self, config: Dict[Any, Any], valid: Dict[Any, Any]) -> None:
        config_copy = config.copy()
        for key, value in list(config_copy.items()):
            if type(value) is dict:
                try:
                    self.validate_cfg(config_copy[key], valid[key])
                except KeyError:
                    raise SyntaxError(f"key {key} is not in VALID_CONFIG")
            elif type(value) is not valid[key]:
                warn(
                    f"Value {value} in key {key} is the incorrect type"
                    f" ({type(value)}), must be ({valid[key]})",
                    SyntaxWarning
                )
            del config_copy[key]
        if config_copy != {}:
            warn(
                f"keys: {list(config_copy.keys())} are invalid keys",
                SyntaxWarning
            )
