"""
dayong.cogs.pingpong
~~~~~~~~~~~~~~~~~~~~

A minimal ping command.
"""
from discord.ext.commands import Bot, Cog, Context, command  # type: ignore


class Ping(Cog):
    """Simple ping command for checking the reachability of the bot's host or
    the latency.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        """Log bot information on server connection."""
        print("Bot is ready!")
        print("Bot Name:", self.bot.user)
        print("Bot ID:", self.bot.user.id)

    @command()
    async def ping(self, ctx: Context) -> None:
        """Reply pong and the time it takes for it to reach the user.

        Args:
            ctx (Context): `discord.ext.commands.Context` instance.
        """
        await ctx.send(f"pong! time {round(self.bot.latency *1000)} ms")


def setup(bot: Bot) -> None:
    """The `setup` entry point function for `ping.py`.

    Args:
        bot (Bot): `discord.ext.commands.Bot` instance.
    """
    bot.add_cog(Ping(bot))
