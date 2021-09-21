"""
dayong.config
~~~~~~~~~~~~~

Initial setup and configuration logic.
"""
import json
import os

from pydantic import BaseModel

from dayong.settings import CONFIG_FILE


class DayongConfigLoader:
    def __init__(self) -> None:
        self.load_cfg()
        self.load_env()

    def load_cfg(self) -> None:
        """Load comments, flags, settings, and paths from config file."""
        with open(CONFIG_FILE, encoding="utf-8") as cfp:
            config = dict(json.load(cfp))
        self.bot_prefix = config["bot_prefix"]

    def load_env(self) -> None:
        """Load environment variables."""
        self.bot_token = os.environ["BOT_TOKEN"]
        self.database_uri = os.environ["DATABASE_URI"]


class DayongConfig(BaseModel):
    bot_prefix: str
    bot_token: str
    database_uri: str

    @classmethod
    def load(
        cls,
        bot_prefix: str,
        bot_token: str,
        database_uri: str,
    ) -> "DayongConfig":
        return cls(
            bot_prefix=bot_prefix,
            bot_token=bot_token,
            database_uri=database_uri,
        )
