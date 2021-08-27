"""
dayong.cogs.test
~~~~~~~~~~~~~~~~~~~~

Greets new member of the guild with static message.
"""
from discord.ext.commands import Bot, Cog, Context, command
from discord import Member, utils, Embed, User
from os import getcwd
import json 

with open(getcwd() + "/dayong/embeddings.json") as file:
	embeddings = json.load(file)

class Test(Cog):
	def __init__(self, bot: Bot):
		self.bot = bot 
		
	@command()
	async def test(self, ctx):
		embed = Embed(
			description=embeddings["description"],
			color=embeddings["color"]
			)

		for i in range(len(embeddings["greetings_field"])):
			inner_DICT = embeddings["greetings_field"][str(i)]
			embed.add_field(
			name=inner_DICT["name"],
			value=inner_DICT["value"],
			inline= True
			)	

		await ctx.send("**Maligayang pagdating sa SurPath Hub**, <@!{}>!".format(ctx.author.id))
		await ctx.send(embed=embed)

		
def setup(bot: Bot):
	"""The `setup` entry point function for `test.py`.
    """
	bot.add_cog(Test(Bot))
	

# To do
# Emojis (?)
# Dynamic guild name