import discord
from discord.ext import commands

class Owner(commands.Cog):
	"""
	Contains command that can be used to alter the state of the bot, and can be only used by the owner of the bot.
	"""
	
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command(aliases=["l"], hidden=True)
	@commands.is_owner()
	async def load(self, ctx, *, module):
		"""Loads a module."""
		try:
			self.bot.load_extension(f"cogs.{module}")
		except Exception:
			await ctx.message.add_reaction("\N{NEGATIVE SQUARED CROSS MARK}")
		else:
			await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')

	@commands.command(aliases=["u"], hidden=True)
	@commands.is_owner()
	async def unload(self, ctx, *, module):
		"""Unloads a module."""
		try:
			self.bot.unload_extension(f"cogs.{module}")
		except Exception:
			await ctx.message.add_reaction("\N{NEGATIVE SQUARED CROSS MARK}")
		else:
			await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

	@commands.command(name='reload', aliases=["r"], hidden=True)
	@commands.is_owner()
	async def _reload(self, ctx, *, module: str = None):
		"""Reloads a module."""
		if module is None:
			return await ctx.channel.send("No module name provided.")

		try:
			self.bot.reload_extension(f"cogs.{module}")
		except Exception as e:
			print(e)
			await ctx.message.add_reaction("\N{NEGATIVE SQUARED CROSS MARK}")
		else:
			await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

	@commands.command(name='exit', aliases=["s", "shutdown"], hidden=True)
	@commands.is_owner()
	async def _exit(self, ctx):
		"""Initiate shutdown of bot."""
		await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
		await self.bot.close()
		
def setup(bot):
	bot.add_cog(Owner(bot))
