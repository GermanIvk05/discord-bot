import random
import discord
import aiohttp
import urllib.parse
from datetime import datetime
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class Utills(commands.Cog):
	"""
	Contains commands which help you in some simple tasks.
	"""

	def __init__(self, bot):
		self.bot = bot

	def parseServerRegion(self, serverLocation):
		if "vip" in serverLocation:
			if serverLocation == "vip-us-east":
				return "VIP US East"
			elif serverLocation == "vip-us-west":
				return "VIP US West"
			return "VIP Amsterdam"
		region = serverLocation.replace("-", " ")
		if " " in region:
			regionSplit = region.split(" ")
			return f"{regionSplit[0].upper()} {regionSplit[1].title()}"
		return region.title()
        
	@commands.command(name="isgd")
	@commands.cooldown(1, 15.0, BucketType.user)
	async def isgd(self, ctx, *, url):
		"""Shortens the url provided by you."""
		async with aiohttp.ClientSession() as sess:
			async with sess.get(f"http://is.gd/create.php?format=simple&url={urllib.parse.quote(url)}") as resp:
				text = await resp.text()
		if "error" in text.lower():
			embed = discord.Embed(description=f"{text}", color=0xFF4897)
			return await ctx.channel.send(embed=embed)
		embed = discord.Embed(description=f"Your shortened URL is **<{text}>**", color=0xFF4897)
		await ctx.channel.send(embed=embed)

	@commands.command(name="avatar", aliases=["pfp"])
	async def _avatar(self, ctx, *, user: discord.User = None):
		"""Displays a users avatar/profile picture."""
		if user is None:
			user = ctx.author
		embed = discord.Embed(title=f"{user.name}'s Avatar", color=0xFF4897)
		embed.set_image(url=user.avatar_url)
		await ctx.channel.send(embed=embed)

	@commands.command(name="ping", aliases=["latency"])
	async def _ping(self, ctx):
		"""Latency and API response times."""
		emoji = "\N{TABLE TENNIS PADDLE AND BALL}"
		sentMessage = await ctx.channel.send("\N{TABLE TENNIS PADDLE AND BALL} Pong! (Calculating Ping).")
		pingInMs = int((sentMessage.created_at - ctx.message.created_at).microseconds/1000)
		await sentMessage.edit(content=f"{emoji} Pong! **WS Latency:** `{int(self.bot.latency*1000)}`ms. **Roundtrip (User <-> Bot):** `{pingInMs}`ms.")
    
	@commands.command(name="choose")
	async def _choose(self, ctx, *, things: str = None):
		"""Make me choose between a comma separated list of things."""
		if things is None:
			return await ctx.channel.send("Please give some things to choose from.")
		listOfThings = [i for i in things.split(",") if i]
		if len(listOfThings) == 1:
			return await ctx.channel.send(f"I would choose **{listOfThings[0]}** as that is the only thing.")
		randomChoice = random.choice(listOfThings)
		await ctx.channel.send(f"I choose: **{randomChoice}**.")
		
	@commands.command(name="hastebin")
	async def _hastebin(self, ctx, *, text: str = None):
		"""Upload some text to hastebin."""
		if text is None:
			return await ctx.channel.send("Please provide some text.")

		def _cleanup_code(content):
			if content.startswith('```') and content.endswith('```'):
				return '\n'.join(content.split('\n')[1:-1])
			return content.strip('` \n')

		text=_cleanup_code(text)
		async with aiohttp.ClientSession() as sess:
			async with sess.post("https://hastebin.com/documents", data=text.encode("utf-8")) as post:
				json = await post.json()
		url = f"https://hastebin.com/{json['key']}"
		embed = discord.Embed(title="HasteBin", description=f"Your file has been uploaded [here]({url})", color=0xFF4897)
		await ctx.channel.send(embed=embed)

	@commands.command(name="userinfo", aliases=["uinfo", "person"])
	@commands.guild_only()
	async def userinfo(self, ctx, *, user: discord.Member = None):
		"""Show a user's information."""
		if user is None:
			user = ctx.author
		status = str(user.status).title()
		if status == "Dnd":
			status = "Do Not Disturb"
		info = f"""**Name:** {user.name}
			**Discriminator:** {user.discriminator}
			**Bot:** {user.bot}
			**ID:** `{user.id}`
			**Status:** {status}
			**Nickname:** {user.nick}
			**Created At:** {user.created_at.strftime("%A, %B %d, %Y.")}
			**Joined Guild At:** {user.joined_at.strftime("%A, %B %d, %Y.")}
			**Roles [{len(user.roles)}]:** `{", ".join([x.name for x in user.roles])}`"""
		embed = discord.Embed(description=info, color=0xFF4897)
		embed.set_author(name=str(user), icon_url=user.avatar_url)
		embed.set_thumbnail(url=user.avatar_url)
		await ctx.channel.send(embed=embed)

	@commands.command(name="serverinfo", aliases=["serverstats", "guildinfo", "guildstats", "sinfo"])
	@commands.guild_only()
	async def serverinfo(self, ctx):
		"Displays server information and statistics."
		region = self.parseServerRegion(str(ctx.guild.region))
		info = f"""**Owner:** {ctx.guild.owner.name}
			**Owner ID:** `{ctx.guild.owner.id}`
			**Server ID:** `{ctx.guild.id}`
			**Region:** {region}
			**Created At:** {ctx.guild.created_at.strftime("%A, %B %d, %Y.")}
			**Roles:** {len(ctx.guild.roles)}
			**Member Count:** {len([x for x in ctx.guild.members if not x.bot])} ({len([x for x in ctx.guild.members if x.bot])} bots)
			**Members Online:** {len([x for x in ctx.guild.members if not str(x.status) == "offline"])}"""
		embed = discord.Embed(description=info, color=0xFF4897)
		embed.set_author(name=ctx.guild.name)
		if ctx.guild.icon_url:
			embed.set_thumbnail(url=ctx.guild.icon_url)
		await ctx.channel.send(embed=embed)
    
	@commands.command(name="channelinfo", aliases=["cinfo", "channel"])
	async def channelinfo(self, ctx, channel: discord.TextChannel = None):
		"""Displays information about a text channel."""
		if channel is None:
			channel =  ctx.channel
		info = f"""**ID:** {channel.id}
			**Category:** {str(channel.category)}
			**NSFW:** {channel.is_nsfw()}
			**Created At:** {channel.created_at.strftime("%A, %B %d, %Y.")}
			**Topic:** {channel.topic}"""
		embed = discord.Embed(title=channel.name, description=info, color=0xFF4897)
		await ctx.channel.send(embed=embed)


	@commands.command(name="emotes", aliases=["emojis", "emoticon"])
	@commands.guild_only()
	async def _emotes(self, ctx):
		"""Shows all the custom emotes of the server."""
		customEmotes = ctx.guild.emojis
		if not customEmotes:
			return await ctx.channel.send("There are no custom emotes in this server.")
		rendered = [str(x) for x in customEmotes]
		renderedString = " ".join(rendered)
		await ctx.channel.send(renderedString)

def setup(bot):
	bot.add_cog(Utills(bot))
