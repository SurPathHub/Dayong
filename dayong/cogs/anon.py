"""
dayong.cogs.anon
~~~~~~~~~~~~~~~~

This module allows users or members to send anonymous messages on Discord.
"""
from discord import Embed, TextChannel  # type: ignore
from discord.ext.commands import Bot, Cog, Context, command  # type: ignore
from discord.message import Message  # type: ignore

from dayong.bot import EMBEDDINGS


class AnonymousMessage(Cog):
    """Cog containing commands for sending anonymous messages."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener("on_message")
    async def anon_message(self, message: Message) -> None:
        """Delete original message and temporarily save it for moderation.

        Args:
            message (Message): `discord.message.Message` instance.
        """
        prefix = await self.bot.get_prefix(message)
        prefix_cmd = f"{prefix}anon"
        content = str(message.content)

        if content.startswith(prefix_cmd) and isinstance(
            message.channel,
            TextChannel,
        ):
            await message.delete()

    @command(name="anon")
    async def anon_command(self, ctx: Context, *messages):
        """Send anonymized user or member message.

        This will keep the author anonymous on public channels, though it
        isn't guaranteed. There will be a slight time delay between the
        deletion of the original message and the delivery of the anonymized
        message.

        Args:
            ctx (Context): `discord.ext.commands.Context` instance.
        """
        if isinstance(ctx.channel, TextChannel):
            embed = Embed(
                title="From Anon",
                description=f"`{' '.join(messages)}`",
                color=EMBEDDINGS["color"],
            )
            await ctx.send(embed=embed)


def setup(bot: Bot) -> None:
    """The `setup` entry point function for `anon.py`.

    Args:
        bot (Bot): `discord.ext.commands.Bot` instance.
    """
    bot.add_cog(AnonymousMessage(bot))
