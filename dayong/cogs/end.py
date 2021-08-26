"""
dayong.cogs.end
~~~~~~~~~~~~~~~~~~~~

Terminates the bot from running.
"""
from discord.ext.commands import Bot, Cog, Context, command, is_owner

class End(Cog):
	def __init__(self, bot: Bot):
		self.bot = bot 

	@command()
	@is_owner()
	async def end(self, ctx):
		""" Terminates the bot from processing.
			This can only be done if you have the ownership.
		"""
		await ctx.send("Process terminated.")
		await ctx.bot.logout()
		
def setup(bot: Bot):
	"""The `setup` entry point function for `end.py`.
    """
	bot.add_cog(End(Bot))