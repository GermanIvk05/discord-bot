#!/usr/bin/python3

import random
import aiohttp
import discord
import datetime
import functools
from bs4 import BeautifulSoup
from discord.ext import commands

class Client:
    
    def __init__(self, bot):
        self.bot = bot
        self.garfieldURL = "https://d1ejxu6vysztl5.cloudfront.net/comics/garfield"
    
    #Allow us to get todays garfield comic strip or a random date.    
    def getGarfieldDate(self, mode):
        
        #If mode is equel to 0, then we get a random date and return a link to gif image.
        if mode == 0:
            year = random.randint(1979, datetime.date.today().year)
            month = random.randint(1, 12)
            
            if month < 10:
                month = f"0{month}"
                
            day = random.randint(1, 28)
            
            if day < 10:
                day = f"0{day}"
                
            return f"{self.garfieldURL}/{year}/{year}-{month}-{day}.gif"
        
        #If mode is not equel to 0, then else par is active (we get today's comic and return a link.)
        else:
            today = datetime.date.today()
            month = today.month
            day = today.day
            
            if month < 10:
                month = f"0{month}"
                
            if day < 10:
                day = f"0{day}"
                
            return f"{self.garfieldURL}/{today.year}/{today.year}-{month}-{day}.gif"
    
    #Getting Garfield comir and returnoing url.        
    async def getGarfield(self, mode):
        """Get a Garfield comic."""
        func = functools.partial(self.getGarfieldDate, mode)
        url = await self.bot.loop.run_in_executor(None, func)
        return url

class Comic(commands.Cog):
    """Read the Garfield comic strips published today, or fetch comic by random date."""
    
    def __init__(self, bot):
        self.bot = bot
        self.comicClient = Client(bot)
    
    #Creating garfield command.
    #Setting rules to use command in guild only
    @commands.command()
    @commands.guild_only()
    async def garfield(self, ctx, mode: str = None):
        """
        Get a random Garfield Comic Strip or read today's
        Use 'today' flag to get today's comic.
        """
        
        #If mode is today, then we send "mode 1"
        if mode == "today":
            url = await self.comicClient.getGarfield(mode=1)
        
        #If mode is not today, then we send "mode 0"    
        else:
            url = await self.comicClient.getGarfield(mode=0)
            
        embed = discord.Embed(color=0xFF4897)
        embed.set_image(url=url)
        embed.set_author(name="Garfield 📰", url=url)
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Comic(bot))
