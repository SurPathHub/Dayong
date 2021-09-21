import os
from typing import Union

import hikari
import tanjun

from dayong.config import DayongConfig, DayongConfigLoader
from dayong.impls import DatabaseImpl
from dayong.protocols import DatabaseProto
from dayong.settings import BASE_DIR

if os.name != "nt":
    import uvloop

    uvloop.install()


async def get_prefix(
    ctx: tanjun.abc.MessageContext,
    db: DatabaseProto = tanjun.injected(type=DatabaseProto),
) -> Union[list[str], tuple[()]]:
    if ctx.guild_id and (guild_info := await db.get_guild_info(ctx.guild_id)):
        return guild_info.prefixes

    return ()


def fetch_component() -> list[str]:
    """Traverse the components directory and collect component modules.

    This will fetch the module from the components directory, remove its
    extension and convert it to `sys.path`.

    Returns:
        list[str]: Sequence of python modules.
    """
    extensions: list[str] = []
    components = os.path.join(BASE_DIR, "components")

    for file in os.listdir(components):
        if file.endswith(".py") and "__" not in file:
            file = f"components.{file}".replace(".py", "")
            extensions.append(file)

    return extensions


def run() -> None:
    """Run Dayong using configs and deps."""
    loaded_config = DayongConfig(**DayongConfigLoader().__dict__)
    bot = hikari.GatewayBot(loaded_config.bot_token)
    (
        tanjun.Client.from_gateway_bot(bot)
        .load_modules(*fetch_component())
        .add_prefix(loaded_config.bot_prefix)
        .set_prefix_getter(get_prefix)
        .set_type_dependency(DayongConfig, lambda: loaded_config)
        .set_type_dependency(
            DatabaseProto,
            tanjun.cache_callback(DatabaseImpl.connect),
        )
    )
    bot.run()


if __name__ == "__main__":
    run()
