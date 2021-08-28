"""
dayong.cogs.greetings
~~~~~~~~~~~~~~~~~~~~

Greets new member of the guild.
"""
import json
from os import getcwd

from discord import Embed, Member, utils
from discord.ext.commands import Bot, Cog

with open(getcwd() + "/dayong/embeddings.json", "r", encoding="utf-8") as file:
    embeddings = json.load(file)


class Greetings(Cog):
    """
    Greets new member of the guild.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener("on_member_join")
    async def welcome_member(self, member: Member):
        """
        This is called when a new member arrived on the server
        """
        channel = utils.get(
            member.guild.channels,
            name=embeddings["greetings_channel"],
        )

        embed = Embed(
            description=embeddings["description"].format(
                member.guild, member.id, embeddings["readme_channel_id"]
            ),
            color=embeddings["color"],
        )

        for i in range(len(embeddings["greetings_field"])):
            inner_dict = embeddings["greetings_field"][str(i)]
            embed.add_field(
                name=inner_dict["name"], value=inner_dict["value"], inline=True
            )

        await channel.send(embed=embed)


def setup(bot: Bot):
    """The `setup` entry point function for `test.py`."""
    bot.add_cog(Greetings(Bot))
