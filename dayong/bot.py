"""
This module defines the setup logic for Dayong.
"""
import json
import os
import sys
from pathlib import Path
from typing import Any

from discord import Intents
from discord.ext.commands import Bot
from discord.ext.commands.errors import (
    ExtensionAlreadyLoaded,
    ExtensionFailed,
    ExtensionNotFound,
    NoEntryPointError,
)
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

# Parse the .env file and load the environment variables.
load_dotenv()

# Load any environment variables or secrets necessary for Dayong to run.
BOT_PREFIX = os.getenv("BOT_PREFIX")
TOKEN = os.getenv("YOUR_BOT_TOKEN_HERE")
APPLICATION_ID = os.getenv("APPLICATION_ID")
OWNERS = os.getenv("OWNERS").split(",")


def load_config_file() -> Any:
    """Parse the `config.json` file from the project root directory.

    Returns:
        Any: The key-value pair contained in the file.
    """
    config_file = "config.json"
    if not os.path.isfile(os.path.join(ROOT_DIR, config_file)):
        sys.exit(f"'{config_file}' cannot be found!")

    with open(config_file, "r", encoding="utf-8") as cfp:
        return json.load(cfp)


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


def setup_bot(use_config: bool = False) -> None:
    """Run Dayong with the configuration specified in either the `config.json`
    or `.env` file.

    The keys in the config file are as listed here:
    - bot_prefix (string)
    - token (string)
    - application_id (string)
    - owners (array[number])

    This bot uses default intents (events restrictions). For more information
    on intents, please refer to discord.py's documentation:
    - https://discordpy.readthedocs.io/en/latest/intents.html

    Args:
        use_config (bool, optional): If True, use the `config.json` file from
            the project root directory. Defaults to using environment
            variables.
    """
    if use_config is True:
        conf = load_config_file()
        conf_prefix = conf["bot_prefix"]
        conf_token = conf["token"]
    else:
        conf_prefix = BOT_PREFIX
        conf_token = TOKEN

    exts = load_extensions()
    bot = Bot(conf_prefix, intents=Intents.default())

    for ext in exts:
        try:
            bot.load_extension(f"cogs.{ext}")
            print(f"Loaded extension '{ext}'")
        except ExtensionNotFound:
            pass
        except ExtensionAlreadyLoaded:
            pass
        except NoEntryPointError:
            pass
        except ExtensionFailed:
            pass

    bot.run(conf_token)


if __name__ == "__main__":
    setup_bot()
