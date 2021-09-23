"""
dayong.configs
~~~~~~~~~~~~~~

Initial setup and configuration logic.
"""
import json
import os

from pydantic.main import BaseModel

from dayong.settings import CONFIG_FILE


class DayongConfigLoader:
    """Configuration loader for Dayong."""

    def __init__(self) -> None:
        self.load_cfg()
        self.load_env()

    def load_cfg(self) -> None:
        """Load comments, flags, settings, and paths from config file."""
        with open(CONFIG_FILE, encoding="utf-8") as cfp:
            config = dict(json.load(cfp))
        self.bot_prefix = config["bot_prefix"]
        self.guild_id = config["guild_id"]
        self.embeddings = config["embeddings"]

    def load_env(self) -> None:
        """Load environment variables."""
        self.bot_token = os.environ["BOT_TOKEN"]
        self.database_uri = os.environ["DATABASE_URI"]


class DayongConfig(BaseModel):
    """Data model for Dayong's configuration."""

    bot_prefix: str
    bot_token: str
    database_uri: str
    guild_id: int
    embeddings: dict

    @classmethod
    def load(
        cls,
        bot_prefix: str,
        bot_token: str,
        database_uri: str,
        guild_id: int,
        embeddings: dict,
    ) -> "DayongConfig":
        """Constructor for DayongConfig.

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
