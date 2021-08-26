"""
dayong.cogs.devtools
~~~~~~~~~~~~~~~~~~~~

This extension provides utilities for managing extensions used by Dayong.
"""
from typing import Union

from discord.ext.commands import Bot, Cog, Context, command, is_owner  # type: ignore
from discord.ext.commands.errors import (  # type: ignore
    CommandError,
    CommandInvokeError,
    DiscordException,
)


class Utility(Cog):
    """Class containing commands for managing bot extensions or cogs."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.ext = ""

    async def handle_ext_error(
        self,
        error: DiscordException,
    ) -> Union[str, None]:
        """Callback method for handling extension errors.

        Instead of checking the exception type to determine the error and
        execute approriate actions, this uses the string representation of
        `CommandInvokeError`.

        Args:
            error (DiscordException): An instance of `DiscordException`.

        Returns:
            Union[str, None]: A helpful message related to the error, None if
                the exception isn't extension related.
        """
        error = str(error)
        error_msg = f"```python\n{error}\n```"
        reply_msg = f"Failed to load {self.ext}."

        if "ExtensionNotFound" in error:
            tip = "Unable to find"
            return f"{tip} {self.ext}\n{error_msg}"
        if "NoEntryPointError" in error:
            tip = "Check its `setup` entry point."
            return f"{reply_msg} {tip}\n{error_msg}"
        if "ExtensionFailed" in error:
            tip = "Check its module or `setup` entry point"
            return f"{reply_msg} {tip}.\n{error_msg}"
        if "ExtensionAlreadyLoaded" in error:
            pass
        if "ExtensionNotLoaded" in error:
            pass

        return None

    async def manage_ext(
        self,
        _load: bool = False,
        _unload: bool = False,
        unload_load: bool = False,
    ) -> None:
        """Load or _unload the specified extension.

        Args:
            ext (str): The extension name.
            _load (bool, optional): If True, load the extension. Defaults to
                False.
            _unload (bool, optional): If True, unload the extension. Defaults
                to False.
            unload_load (bool, optional): If True, perform an unload-load
                operation. Defaults to False.
        """
        if _load:
            self.bot.load_extension(self.ext)
            return
        if _unload:
            self.bot.unload_extension(self.ext)
            return
        if unload_load:
            self.bot.unload_extension(self.ext)
            self.bot.load_extension(self.ext)
            return

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        """Listener for incoming commands.

        Args:
            ctx (Context): Context in which a command is being invoked under.
            error (str): [description]
        """
        if isinstance(error, CommandInvokeError):
            message = await self.handle_ext_error(error)
            await ctx.send(message)

    @command()
    async def load(self, ctx: Context, ext: str) -> None:
        """Load specified extension from the cogs directory.

        Args:
            ctx (Context): `discord.ext.commands.Context` object.
            ext (str): The extension name.
        """
        self.ext = f"cogs.{ext}"
        await self.manage_ext(_load=True)
        await ctx.send(f"Loaded {self.ext}!")

    @command()
    async def unload(self, ctx: Context, ext: str) -> None:
        """Unload specified extension.

        Args:
            ctx (Context): `discord.ext.commands.Context` object.
            ext (str): The extension name.
        """
        self.ext = f"cogs.{ext}"
        await self.manage_ext(_unload=True)
        await ctx.send(f"Unloaded {self.ext}!")

    @command()
    async def reload(self, ctx: Context, ext: str) -> None:
        """Reload specified extension.

        Args:
            ctx (Context): `discord.ext.commands.Context` object.
            ext (str): The extension name.
        """
        self.ext = f"cogs.{ext}"
        await self.manage_ext(unload_load=True)
        await ctx.send(f"Reloaded {self.ext}!")

    @command()
    @is_owner()
    async def end(self, ctx):
        """ Terminates the bot from processing.
            This can only be done if you're an owner of the Bot.
        """
        await ctx.send("Process terminated.")
        await ctx.bot.close()


def setup(bot: Bot) -> None:
    """The `setup` entry point function for `utils.py`.

    Args:
        bot (Bot): `discord.ext.commands.Bot` instance.
    """
    bot.add_cog(Utility(bot))
