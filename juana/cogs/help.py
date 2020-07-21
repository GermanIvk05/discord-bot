import os
import discord
from inspect import getdoc
from datetime import datetime
from discord.ext import commands
from collections import defaultdict


class Help(commands.Cog):
	"""
	See information about other categories and commands.
	"""

	def __init__(self, bot):
		self.bot = bot
		bot.remove_command("help")

	async def _can_run(self, cmd, ctx):
		try:
			return await cmd.can_run(ctx)
		except Exception:
			return False

	async def BotEmbed(self, ctx):
		registeredCommands = list(self.bot.commands)
		plausibleCommands = [cmd for cmd in registeredCommands if (await self._can_run(cmd, ctx)) and not cmd.hidden]
		cogs_dict = defaultdict(list)
		for i in plausibleCommands:
			cogs_dict[i.cog_name].append(f"`{i.name}`")
		editedCogNames = "\n".join([f"• **{x}**" for x in sorted(list(cogs_dict.keys()), key=lambda c: c)])
		desc = f"Type `{ctx.prefix}help <category>` for detailed help about a particular category.\n{editedCogNames}"
		helpEmbed = discord.Embed(title=f"{self.bot.user.name}'s Command Categories", description=desc, color=0xFF4897)
		helpEmbed.set_footer(text=f"{self.bot.user.name} {datetime.utcnow().year}. Licensed under MIT license.", icon_url=self.bot.user.avatar_url)
		return helpEmbed

	async def CategoryEmbed(self, cog, ctx):
		cog_name = cog.__class__.__name__
		cogCommands = sorted([x for x in list(self.bot.get_cog(cog_name).get_commands()) if (await self._can_run(x, ctx)) and not x.hidden], key=lambda c: c.name)
		if not cogCommands:
			return discord.Embed(title="Error!", description="You cannot run any commands present in the category.", color=0xFF4897)
		cogHelp = "\n".join([f"**{x.name}:** `{x.help}`" for x in cogCommands])
		desc = f"```{getdoc(cog)}```\n{cogHelp}"
		return discord.Embed(title=f"{cog_name}'s commands", description=desc, color=0xFF4897)

	@commands.command(name="help", aliases=["h", "cmds"])
	async def _help(self, ctx, *, commandName: str = None):
		"""Shows this message."""
		if commandName is None:
			embed = await self.BotEmbed(ctx)
			return await ctx.channel.send(embed=embed)
		entity = self.bot.get_cog(commandName)
		if not entity:
			embed = discord.Embed(title="Error!", description="Category not found! Please check spelling of category.", color=0xFF4897)
			return await ctx.channel.send(embed=embed)
		else:
			embed = await self.CategoryEmbed(entity, ctx)
		await ctx.channel.send(embed=embed)

def setup(bot):
	bot.add_cog(Help(bot))
