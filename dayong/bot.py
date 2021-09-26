"""
dayong.bot
~~~~~~~~~~

This module defines the startup logic for Dayong.
"""
import os
from pathlib import Path

import hikari
import tanjun

from dayong.configs import DayongConfig, DayongConfigLoader
from dayong.impls import MessageDBImpl
from dayong.settings import BASE_DIR


def run() -> None:
    """Run Dayong with configs and deps."""
    loaded_config = DayongConfigLoader.load()
    bot = hikari.GatewayBot(
        loaded_config.bot_token,
        banner="dayong",
        intents=hikari.Intents.ALL,
    )
    (
        tanjun.Client.from_gateway_bot(
            bot, set_global_commands=hikari.Snowflake(loaded_config.guild_id)
        )
        .load_modules(*Path(os.path.join(BASE_DIR, "components")).glob("*.py"))
        .add_prefix(loaded_config.bot_prefix)
        .set_type_dependency(DayongConfig, lambda: loaded_config)
        .set_type_dependency(
            MessageDBImpl, tanjun.cache_callback(MessageDBImpl.connect)
        )
    )
    bot.run()
