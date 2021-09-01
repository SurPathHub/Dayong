"""
dayong.cogs.greetings
~~~~~~~~~~~~~~~~~~~~~

Greets new member of the guild.
"""
from discord import Embed, Member, utils  # type: ignore
from discord.ext.commands import Bot, Cog  # type: ignore

from dayong.bot import EMBEDDINGS


class Greetings(Cog):
    """
    Greets new member of the guild.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener("on_member_join")
    async def welcome_member(self, member: Member):
        """
        This is called when a new member arrives on the server.
        """
        channel = utils.get(
            member.guild.channels,
            name=EMBEDDINGS["greetings_channel"],
        )

        embed = Embed(
            description=EMBEDDINGS["description"].format(
                member.guild, member.id, EMBEDDINGS["readme_channel_id"]
            ),
            color=EMBEDDINGS["color"],
        )

        for i in range(len(EMBEDDINGS["greetings_field"])):
            inner_dict = EMBEDDINGS["greetings_field"][str(i)]
            embed.add_field(
                name=inner_dict["name"], value=inner_dict["value"], inline=True
            )

        await channel.send(embed=embed)


def setup(bot: Bot):
    """The `setup` entry point function for `test.py`."""
    bot.add_cog(Greetings(Bot))
