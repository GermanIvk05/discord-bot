#!/usr/bin/python3

import aiohttp
import discord
from discord.ext import commands

class Animals(commands.Cog):
    """Containst commands to view random images of animals/wildlife."""
    
    def __init__(self, bot):
        self.bot = bot
        
    #Creating a dog command.
    #Setting rule to use command in guild only.
    @commands.command(name="dog", aliases=["puppy", "doge"])
    @commands.guild_only()
    async def dog(self, ctx):
        """Get a random dog image."""
        
        #Setting up url variable.
        url = "http://dog.ceo/api/breeds/image/random"
        
        #Getting image through json.
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url) as resp:
                json = await resp.json()
        
        #Setting discord.Embed as embed and setting color.        
        embed = discord.Embed(title="Random Dog 🐶", color=0xFF4897)
        embed.set_image(url=json["message"])
        return await ctx.channel.send(embed=embed)
        
    #Creating a bird command.
    #Setting rule to use command in guild only.
    @commands.command(name="bird", aliases=["birb", "ave"])
    @commands.guild_only()
    async def bird(self, ctx):
        """Get a random bird image."""
        
        #Setting up url variable.
        url = "http://shibe.online/api/birds"
        
        #Getting image through json.
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url) as resp:
                json = await resp.json()
                
        #Setting discord.Embed as embed and setting color.
        embed = discord.Embed(title="Random Bird 🐦", color=0xFF4897)
        embed.set_image(url=json[0])
        return await ctx.channel.send(embed=embed)
       
    #Creating a cat command.
    #Setting rule to use command in guild only.
    @commands.command(name="cat", aliases=["kitten", "kitty"])
    @commands.guild_only()
    async def cat(self, ctx):
        """Get a random cat image."""
        
        #Setting up url variable.
        url = "http://shibe.online/api/cats"
        
        #Getting image through json.
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url) as resp:
                json = await resp.json()
                
        #Setting discord.Embed as embed and setting color.
        embed = discord.Embed(title="Random Cat 🐱", color=0xFF4897)
        embed.set_image(url=json[0])
        return await ctx.channel.send(embed=embed)
       
    #Creating a shibe command.
    #Setting rule to use command in guild only.
    @commands.command(name="shibe", aliases=["shiba", "inu"])
    @commands.guild_only()
    async def shibe(self, ctx):
        """Get a random shiba inu dog image."""
        
        #Setting up url variable.
        url = "http://shibe.online/api/shibes"
        
        #Getting image through json.
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url) as resp:
                json = await resp.json()
                
        #Setting discord.Embed as embed and setting color.
        embed = discord.Embed(title="Random Shibe 🐕", color=0xFF4897)
        embed.set_image(url=json[0])
        return await ctx.channel.send(embed=embed)
         
    #Creating a fox command.
    #Setting rule to use command in guild only.
    @commands.command(name="fox")
    @commands.guild_only()
    async def fox(self, ctx):
        """Get a random fox image."""
        
        #Setting up url variable.
        url = "http://randomfox.ca/floof/"
        
        #Getting image through json.
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url) as resp:
                json = await resp.json()
        
        #Setting discord.Embed as embed and setting color.
        embed = discord.Embed(title="Random Fox 🦊", color=0xFF4897)
        embed.set_image(url=json["image"])
        return await ctx.channel.send(embed=embed)
       
def setup(bot):
    bot.add_cog(Animals(bot))
