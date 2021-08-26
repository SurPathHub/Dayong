"""
dayong.cogs.greetings
~~~~~~~~~~~~~~~~~~~~

Greets new member of the guild with static message.
"""
from discord.ext.commands import Bot, Cog, Context, command
from discord import Member, utils, Embed
from os import getcwd
import json 

with open(getcwd() + "/dayong/embeddings.json") as file:
	embeddings = json.load(file)


class Greet(Cog):
	def __init__(self, bot: Bot):
		self.bot = bot 

	@Cog.listener()
	async def on_member_join(self, member: Member):
		""" Greets new member of the guild.
		"""
		channel = utils.get(member.guild.channels, name = "welcome")
		await channel.send("Welcome @{0.name}.".format(member))
		
	@command()
	async def greet(self, ctx):
		#embed = Embed.from_dict(embeddings["greet"])
		await ctx.send(embeddings["greet"])
		
def setup(bot: Bot):
	"""The `setup` entry point function for `greetings.py`.
    """
	bot.add_cog(Greet(Bot))