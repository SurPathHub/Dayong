"""
dayong.bot
~~~~~~~~~~

This module defines the startup logic for Dayong.
"""
import os
from pathlib import Path

import hikari
import tanjun

from dayong.configs import DayongConfig, DayongDynamicLoader
from dayong.impls import MessageDBImpl
from dayong.interfaces import MessageDBProto
from dayong.settings import BASE_DIR


def run() -> None:
    """Run Dayong with configs and deps."""
    loaded_config = DayongDynamicLoader.load()
    bot = hikari.GatewayBot(
        loaded_config.bot_token,
        banner="dayong",
        intents=hikari.Intents.ALL,
    )
    database = MessageDBImpl()
    (
        tanjun.Client.from_gateway_bot(
            bot, declare_global_commands=hikari.Snowflake(loaded_config.guild_id)
        )
        .load_modules(*Path(os.path.join(BASE_DIR, "components")).glob("*.py"))
        .add_prefix(loaded_config.bot_prefix)
        .set_type_dependency(DayongConfig, loaded_config)
        .set_type_dependency(MessageDBProto, database)
        .add_client_callback(tanjun.ClientCallbackNames.STARTING, database.connect)
    )
    bot.run()
