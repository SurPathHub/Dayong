"""
dayong.cogs.devtools
~~~~~~~~~~~~~~~~~~~~

This extension provides utilities for managing extensions used by Dayong.
"""
from functools import wraps

from discord.ext.commands import Bot, Cog, Context, command  # type: ignore
from discord.ext.commands.errors import (  # type: ignore
    ExtensionAlreadyLoaded,
    ExtensionFailed,
    ExtensionNotFound,
    ExtensionNotLoaded,
    NoEntryPointError,
)


def ext_exception_handler(func):
    """Handle any raised `discord.ext.commands.errors.ExtensionError`
    subclass.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        async def tmp():
            failed_msg = "Failed to load {ext}. "
            try:
                await func(*args, **kwargs)
            except ExtensionNotFound as enf:
                return (
                    "Unable to find {ext}",
                    f"```python\n{enf}\n```",
                )
            except NoEntryPointError as npe:
                return (
                    failed_msg + "Check its `setup` entry point.",
                    f"```python\n{npe}\n```",
                )
            except ExtensionFailed as efe:
                return (
                    failed_msg + "Check its module or `setup` entry point.",
                    f"```python\n{efe}\n```",
                )
            except ExtensionAlreadyLoaded:
                pass
            except ExtensionNotLoaded:
                pass

        return tmp()

    return wrapper


class Utility(Cog):
    """Simple ping command for checking the reachability of the bot's host or
    the latency.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @ext_exception_handler
    async def manage_ext(
        self,
        ext: str,
        _load: bool = False,
        _unload: bool = False,
    ) -> None:
        """Load or _unload the specified extension.

        Args:
            ext (str): The extension name.
            _load (bool, optional): If True, load the extension. Defaults to
                False.
            _unload (bool, optional): If True, unload the extension. Defaults
                to False.
        """
        if _load:
            self.bot.load_extension(ext)
        if _unload:
            self.bot.unload_extension(ext)

    @command()
    async def load(self, ctx: Context, ext: str) -> None:
        """Load specified extension from the cogs directory.

        Args:
            ctx (Context): `discord.ext.commands.Context` object.
            ext (str): The extension name.
        """
        ext = f"cogs.{ext}"
        res = await self.manage_ext(ext, _load=True) or f"Loaded {ext}!"
        ctx.send(res)

    @command()
    async def unload(self, ctx: Context, ext: str) -> None:
        """Unload specified extension.

        Args:
            ctx (Context): `discord.ext.commands.Context` object.
            ext (str): The extension name.
        """
        ext = f"cogs.{ext}"
        res = await self.manage_ext(ext, _unload=True) or f"Unloaded {ext}!"
        ctx.send(res)

    @command()
    async def reload(self, ctx: Context, ext: str) -> None:
        """Reload specified extension.

        Args:
            ctx (Context): `discord.ext.commands.Context` object.
            ext (str): The extension name.
        """
        ext = f"cogs.{ext}"
        res = (
            await self.manage_ext(
                ext,
                _load=True,
                _unload=True,
            )
            or f"Reloaded {ext}!"
        )
        ctx.send(res)


def setup(bot: Bot) -> None:
    """The `setup` entry point function for `utils.py`.

    Args:
        bot (Bot): `discord.ext.commands.Bot` instance.
    """
    bot.add_cog(Utility(bot))
