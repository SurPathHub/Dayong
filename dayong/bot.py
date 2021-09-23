"""
dayong.bot
~~~~~~~~~~

This module defines the startup logic for Dayong.
"""
import os
from pathlib import Path
from typing import Union

import hikari
import tanjun

from dayong.interfaces import DatabaseProto
from dayong.settings import BASE_DIR, CONFIG


async def get_prefix(
    ctx: tanjun.abc.MessageContext,
    db: DatabaseProto = tanjun.injected(type=DatabaseProto),
) -> Union[list[str], tuple[()]]:
    if ctx.guild_id and (guild_info := await db.get_guild_info(ctx.guild_id)):
        return guild_info.prefixes

    return ()


def run() -> None:
    """Run Dayong with configs and deps."""
    bot = hikari.GatewayBot(
        CONFIG.bot_token,
        banner="dayong",
        intents=hikari.Intents.ALL,
    )
    (
        tanjun.Client.from_gateway_bot(bot, set_global_commands=CONFIG.guild_id)
        .load_modules(*Path(os.path.join(BASE_DIR, "components")).glob("*.py"))
        .add_prefix(CONFIG.bot_prefix)
    )
    bot.run()
