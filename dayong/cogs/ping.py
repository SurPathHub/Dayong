"""
dayong.cogs.pingpong
~~~~~~~~~~~~~~~~~~~~

A minimal ping command.
"""
from discord import Embed  # type: ignore
from discord.ext.commands import Bot, Cog, Context, command  # type: ignore

from dayong.bot import EMBEDDINGS


class Ping(Cog):
    """Simple ping command for checking the reachability of the bot's host or
    the latency.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener("on_ready")
    async def log_bot_info(self) -> None:
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
        embed = Embed(
            description=f"pong! time {round(self.bot.latency *1000)} ms",
            color=EMBEDDINGS["color"],
        )
        await ctx.send(embed=embed)


def setup(bot: Bot) -> None:
    """The `setup` entry point function for `ping.py`.

    Args:
        bot (Bot): `discord.ext.commands.Bot` instance.
    """
    bot.add_cog(Ping(bot))
