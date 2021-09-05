"""
dayong.bot
~~~~~~~~~~

This module defines the startup logic for Dayong.
"""
import os
from pathlib import Path
from typing import Union

from discord import Intents  # type: ignore
from discord.ext.commands import Bot  # type: ignore
from dotenv import load_dotenv

from dayong.exceptions import exception_handler

# Parse the .env file and load the environment variables.
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
CONFIG_FILE = os.path.join(ROOT_DIR, "config.json")
DATABASE_URI: str
EMBEDDINGS: dict

with open(CONFIG_FILE, encoding="utf-8") as cfp:
    config = json.load(cfp)
    DATABASE_URI = config["database_uri"]
    EMBEDDINGS = config["embeddings"]

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
    def check_configs() -> None:
        """Check if `config.json` exists."""
        if not os.path.isfile(CONFIG_FILE):
            sys.exit(f"config.json missing from {ROOT_DIR}!")

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

    @exception_handler
    def run_dayong(self) -> None:
        """Run Dayong with the configurations and the owner's bot credentials.
        """
        pref = BOT_COMMAND_PREFIX
        exts = self.load_extensions()

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
