import random
import urllib.parse
from datetime import datetime
from datetime import timedelta
from platform import python_version
import discord
import psutil
import aiohttp
from discord.ext import commands


class About(commands.Cog):
    """
    Contains commands which cannot be grouped into other categories.
    """

    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()
        self.smallPyPI = "https://raw.githubusercontent.com/nlhkabu/warehouse-ui/gh-pages/img/pypi-sml.png"
        self.factType = [
			"trivia",
			"year",
			"date",
            "math"
        ]
    
    def getUptime(self):
        delta = timedelta
        hours, rem = divmod(str(int(delta.seconds), 3600))
        minutes, seconds = divmod(rem, 60)
        days, hours = divmod(hours, 24)
        if days:
            return f"{days} days, {hours} hr, {minutes} mins, and {seconds} secs"
        else:
            return f"{hours} hr, {minutes} mins, and {seconds} secs"

    @commands.command(name="country")
    async def _country(self, ctx, *, name: str = None):
        """Shows a countries information, by name."""
        if name is None:
            return await ctx.send("Please provide a country name.")
        query = urllib.parse.quote(name)
        base_url = f"https://restcountries.eu/rest/v2/name/{query}?fullText=true"
        async with aiohttp.ClientSession() as sess:
            async with sess.get(base_url) as response:
                if response.status != 200:
                   return await ctx.send("Invalid country name.")
            response = await response.json()
            flag = "https://api.backendless.com/2F26DFBF-433C-51CC-FF56-830CEA93BF00/473FB5A9-D20E-8D3E-FF01-E93D9D780A00/files/CountryFlagsPng/"
            flag = flag + response[0]["alpha3Code"].lower() + ".png"
            name = response[0]["name"] + " (" + response[0]["alpha3Code"] + ") " + ":flag_" + response[0]["alpha2Code"].lower() + ":"
            basic = "Capital : " + "**" + response[0]["capital"] + "**\n"
            basic = basic + "Region : " + "**" + response[0]["region"] + "**\n"
            basic = basic + "Sub-Region : " + "**" + response[0]["subregion"] + "**\n"
            basic = basic + "Demonym : " + "**" + response[0]["demonym"] + "**\n"
            basic = basic + "Regional Name : " + "**" + response[0]["nativeName"] + "**\n"

            more = "Population : " + "**" + str(response[0]["population"]) + " people**\n"
            more = more + "Area : " + "**" + str(response[0]["area"]) + " sq Km**\n"
            more = more + "Main Timezone : " + "**" + response[0]["timezones"][0] + "**\n"

            currency = response[0]["currencies"][0]["name"] + " (" + response[0]["currencies"][0]["symbol"] + ")"
            
            extend = "Currency : " + "**" + currency + "**\n"
            extend = extend + "Official Languages : " + "**" + response[0]["languages"][0]["name"]
            extend = extend + " (" + response[0]["languages"][0]["nativeName"] + ")"
            if len(response[0]["languages"]) > 1:
                extend = extend + ", " + response[0]["languages"][1]["name"] + " (" + response[0]["languages"][1]["nativeName"] + ")**\n"
            else:
                extend = extend + "**\n"
            cn_embed = discord.Embed(title=name, colour=0x2CACD5)
            cn_embed.set_thumbnail(url=flag)
            cn_embed.add_field(name="❯❯ General Information", value=basic, inline=True)
            cn_embed.add_field(name="❯❯ More Information", value=more, inline=True)
            cn_embed.add_field(name="❯❯ Extended Information", value=extend, inline=False)
            cn_embed.set_footer(icon_url=self.bot.user.avatar_url, text="Powered by RestCountries API.")
            await ctx.send(embed=cn_embed)

    @commands.command(name="pypi")
    async def _pypi(self, ctx, *, package: str = None):
        """Search packages on PyPI."""
        if package is None:
            return await ctx.send("Please state a package to search.")
        URL = f"https://pypi.org/pypi/{package}/json"
        async with aiohttp.ClientSession() as sess:
            async with sess.get(URL) as resp:
                if resp.status == 404:
                    return await ctx.send(f"**ERROR! The package `{package}` wasn't found.**")
                pkgDetails = await resp.json()
        uploadTime = pkgDetails["releases"][pkgDetails["info"]["version"]][0]["upload_time"]
        dtUploadTime = datetime.strptime(uploadTime, "%Y-%m-%dT%H:%M:%S")
        strUploadTime = dtUploadTime.strftime("%d/%m/%Y at %H:%M:%S")
        description = f"""{pkgDetails["info"]["summary"]}
**• Author:** {pkgDetails["info"]["author"]}
**• License:** {pkgDetails["info"]["license"]}
**• Latest Version:** {pkgDetails["info"]["version"]}
**• Last Modified:** {strUploadTime}
**• Project Homepage:** [Click to Visit]({pkgDetails["info"]["home_page"]})
**• Install:** `pip install {pkgDetails["info"]["name"]}`"""
        embed = discord.Embed(description=description)
        embed.set_author(name=pkgDetails["info"]["name"], url=pkgDetails["info"]["project_url"], icon_url=self.smallPyPI)
        embed.set_footer(text=f"Command powered by PyPI API - {self.bot.user.name} {datetime.utcnow().year}.", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="stats")
    async def _stats(self, ctx):
        """Shows some information about the bot."""
        ramUsage = self.process.memory_full_info().uss / 1024**2
        cpuUsage = self.process.cpu_percent() / psutil.cpu_count()
        general = f"""• Servers: **{len(self.bot.guilds)}**
• Users: **{sum(1 for _ in self.bot.get_all_members())}**
• Commands: **{len(self.bot.commands)}**"""
        process = f"""• Memory Usage: **{ramUsage:.2f}MiB**
• CPU Usage: **{cpuUsage:.2f}%**
• Uptime: **{self.getUptime()}**"""     
        system = f"""• Python: **{python_version()}**
• discord.py: **{discord.__version__}**"""
        embed = discord.Embed()
        embed.set_author(name=f"{self.bot.user.name}'s Stats", icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url="https://www.python.org/static/community_logos/python-powered-w-200x80.png")
        embed.set_footer(text=f"MIT License - {self.bot.user.name}, {datetime.utcnow().year}. Made by NightShade256.")
        embed.add_field(name="❯❯ General", value=general, inline=False)
        embed.add_field(name="❯❯ Process", value=process, inline=True)
        embed.add_field(name="❯❯ System", value=system, inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="nfact", aliases=["numberfact"])
    async def _nfact(self, ctx):
        """Displays a fact about a random number."""
        baseURL = f"http://numbersapi.com/random/{random.choice(self.factType)}?json"
        async with aiohttp.ClientSession() as sess:
            async with sess.get(baseURL) as resp:
                json = await resp.json()
        number = str(json["number"])
        await ctx.send(json["text"].replace(number, f"**__{number}__**"))

    @commands.command(name="badge")
    async def _badge(self, ctx, subject: str = None, status: str = None, color: str = None):
        """Create a custom badge."""
        if status is None or subject is None or color is None:
            return await ctx.send("You have to provide all subject, status and color.")
        embed = discord.Embed(color=0x36393E)
        embed.set_image(url=f"https://img.shields.io/badge/{subject}-{status}-{color.lower()}.png")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(About(bot))
