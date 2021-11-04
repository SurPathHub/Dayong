# pylint: disable=R0903
"""
dayong.configs
~~~~~~~~~~~~~~

Initial setup and configuration logic.
"""
import json
import os
from typing import Any, Optional, Union

from pydantic import BaseModel

from dayong.settings import CONFIG_FILE
from dayong.utils import format_db_url


class ConfigFile(BaseModel):
    """Configuration model."""

    bot_prefix: str
    embeddings: dict[str, Union[str, dict[str, Any]]]
    guild_id: int
    imap_domain_name: str


class EnvironVariables(BaseModel):
    """Env model."""

    bot_token: str
    database_uri: str
    email: Optional[str] = None
    email_password: Optional[str] = None


class DayongConfig(EnvironVariables, ConfigFile):
    """Data model for Dayong's configuration."""

    @classmethod
    def load(cls, **kwargs: Any) -> "DayongConfig":
        """Construct an instance of `dayong.configs.DayongConfig`.

        Returns:
            An instance of `dayong.configs.DayongConfig`.
        """
        email = kwargs.get("email")
        email_password = kwargs.get("email_password")
        return cls(
            bot_prefix=kwargs["bot_prefix"],
            bot_token=kwargs["bot_token"],
            database_uri=kwargs["database_uri"],
            embeddings=kwargs["embeddings"],
            email=email if email else None,
            email_password=email_password if email_password else None,
            guild_id=kwargs["guild_id"],
            imap_domain_name=kwargs["imap_domain_name"],
        )


class DayongEnvLoader:
    """Environment variable loader for Dayong."""

    def __init__(self) -> None:
        self.load_env()

    def load_env(self) -> None:
        """Load environment variables."""
        self.bot_token = os.environ["BOT_TOKEN"]
        self.database_uri = format_db_url(os.environ["DATABASE_URL"])
        self.email = os.environ["EMAIL"]
        self.email_password = os.environ["EMAIL_PASSWORD"]


class DayongConfigLoader:
    """Configuration loader for Dayong."""

    def __init__(self) -> None:
        self.load_cfg()

    def load_cfg(self) -> None:
        """Load comments, flags, settings, and paths from config file."""
        with open(CONFIG_FILE, encoding="utf-8") as cfp:
            config = dict(json.load(cfp))

        self.bot_prefix = config["bot_prefix"]
        self.guild_id = config["guild_id"]
        self.embeddings = config["embeddings"]
        self.imap_domain_name = config["imap_domain_name"]


class DayongDynamicLoader:
    """Dayong dynamic loader"""

    @staticmethod
    def load() -> DayongConfig:
        """Load configs into `dayong.configs.DayongConfig`.

        Returns:
            DayongConfig: An instance of `dayong.configs.DayongConfig`.
        """
        return DayongConfig.load(
            **DayongConfigLoader().__dict__ | DayongEnvLoader().__dict__
        )
