"""
dayong.bot
~~~~~~~~~~

This module defines the startup logic for Dayong.
"""
import os
from pathlib import Path
from typing import Any, Union

from discord import Intents  # type: ignore
from discord.ext.commands import Bot  # type: ignore
from dotenv import load_dotenv

from dayong.exceptions import exception_handler

# Parse the .env file and _load the environment variables.
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
CONFIG_FILE = os.path.join(ROOT_DIR, "config.json")

with open(CONFIG_FILE, encoding="utf-8") as conf_file:
    config = json.load(conf_file)
    DB_CONNECTION_URI: str = config["databse_connection_uri"]
    EMBEDDINGS: dict = config["embeddings"]

# Environment variables or secrets.
BOT_COMMAND_PREFIX: Union[str, None] = os.getenv("BOT_COMMAND_PREFIX")
TOKEN: Union[str, None] = os.getenv("TOKEN")
APPLICATION_ID: Union[str, None] = os.getenv("APPLICATION_ID")
OWNERS: Union[str, list, None] = os.getenv("OWNERS")

if isinstance(OWNERS, str) and "," in OWNERS:
    OWNERS = OWNERS.split(",")


class Setup:
    """Base Setup class."""

    dayong: Bot

    @staticmethod
    def load_configs() -> Any:
        """Parse the `config.json` file from the project root directory.

        Returns:
            Any: The key-value pair contained in the file.
        """
        conf = CONFIG_FILE
        if not os.path.isfile(os.path.join(ROOT_DIR, conf)):
            sys.exit(f"Cannot locate {conf}!")

        with open(conf, "r", encoding="utf-8") as cfp:
            conf_data = json.load(cfp)

        return conf_data

    @staticmethod
    def load_extensions() -> list[str]:
        """Traverse the `cogs` directory and collect cog modules.

        Returns:
            list[str]: A list of Python modules. The `.py` extension should be
                omitted.
        """
        extensions: list[str] = []

        for file in os.listdir(os.path.join(BASE_DIR, "cogs")):
            # Append cog modules and ignore dunder files.
            if file.endswith(".py") and "__" not in file:
                extensions.append(file.replace(".py", ""))

        return extensions

    def setup_bot(
        self,
        use_config: bool = False,
    ) -> tuple[Union[Any, str], list[str]]:
        """Load bot prerequisite.

        The keys in the config file are as listed here:
        - bot_command_prefix (string)
        - token (string)
        - application_id (string)
        - owners (array[number])

        This bot uses default intents (events restrictions). For more
        information on intents, please refer to discord.py's documentation:
        - https://discordpy.readthedocs.io/en/latest/intents.html

        Args:
            use_config (bool, optional): If True, use the `config.json` file
                from the project root directory. Defaults to using environment
                variables.
        """
        pref = BOT_COMMAND_PREFIX
        exts = self.load_extensions()

        if use_config is True or pref is None:
            pref = self.load_configs()["credentials"]["bot_command_prefix"]

        return pref, exts

    @exception_handler
    def run_dayong(self, use_config: bool = False) -> None:
        """Run Dayong with the configuration specified in either the
        `config.json` or `.env` file.
        """
        pref, exts = self.setup_bot(use_config=use_config)

        intents = Intents.default()
        intents.members = True  # pylint: disable=E0237

        self.dayong = Bot(pref, intents=intents)

        for ext in exts:
            self.dayong.load_extension(f"cogs.{ext}")

        if TOKEN is None:
            raise Exception("Bot token missing: {TOKEN}")

        self.dayong.run(TOKEN)


if __name__ == "__main__":
    pass
