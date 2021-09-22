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

from dayong.configs import DayongConfig, DayongConfigLoader
from dayong.interfaces import DatabaseProto
from dayong.settings import BASE_DIR


async def get_prefix(
    ctx: tanjun.abc.MessageContext,
    db: DatabaseProto = tanjun.injected(type=DatabaseProto),
) -> Union[list[str], tuple[()]]:
    if ctx.guild_id and (guild_info := await db.get_guild_info(ctx.guild_id)):
        return guild_info.prefixes

    return ()


class DayongSetup:
    def run_gateway_client(self, bot: hikari.GatewayBot, config: DayongConfig):
        """Build Dayong's `tanjun.Client`."""
        (
            tanjun.Client.from_gateway_bot(bot, set_global_commands=config.guild_id)
            .load_modules(*Path(os.path.join(BASE_DIR, "components")).glob("*.py"))
            .add_prefix(config.bot_prefix)
        )

    def run(self) -> None:
        """Run Dayong with configs and deps."""
        config = DayongConfig(**DayongConfigLoader().__dict__)
        self.bot = hikari.GatewayBot(
            config.bot_token,
            banner="dayong",
            intents=hikari.Intents.ALL,
        )
        self.run_gateway_client(self.bot, config)
        self.bot.run()
