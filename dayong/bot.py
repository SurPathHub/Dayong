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

BASE_DIR = Path(__file__).resolve().parent


def load_config_file() -> Any:
    """Parse the configuration file.

    Returns:
        Any: The key-value pair contained in the file.
    """
    config_file = "config.json"
    if not os.path.isfile(os.path.join(BASE_DIR, config_file)):
        sys.exit(f"'{config_file}' cannot be found!")

    with open("config.json", "r", encoding="utf-8") as confile:
        return json.load(confile)


def load_extensions() -> list[str]:
    """Traverse the `cogs` directory and collect cog modules.

    Returns:
        list[str]: A list of Python modules. The `.py` extension should be
            omitted.
    """
    extensions: list[str] = []
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            extensions.append(file.replace(".py", ""))
    return extensions


def setup_bot() -> None:
    """Run Dayong with the configuration specified in the `config.json` file.

    The keys in the config file are as listed here:
    - bot_prefix (string)
    - token (string)
    - application_id (string)
    - owners (array[number])

    This bot uses default intents (events restrictions). For more information
    on intents, please refer to discord.py's documentation:
    - https://discordpy.readthedocs.io/en/latest/intents.html
    """
    conf = load_config_file()
    exts = load_extensions()
    bot = Bot(conf["bot_prefix"], intents=Intents.default())

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

    # Run the bot with the token
    bot.run(conf["token"])


if __name__ == "__main__":
    setup_bot()
