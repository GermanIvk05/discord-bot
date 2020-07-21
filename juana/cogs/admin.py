#!/usr/bin/python3

import discord
from discord.ext import commands


class Admin(commands.Cog):
    """Contains commands for administaration of guild."""

    def __init__(self, bot):
    	self.bot = bot    

    #Creating a ban command.
    #Setting rule to use command in guild only.
    #Doing a check for permissions "ban_members" required.
    @commands.command(name="ban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, *, member : discord.Member = None, reason = None):
        """Provide username or mention a person to ban from guild."""
        
        #Setting discord.Embed as embed and setting color.
        embed = discord.Embed(color = 0x9b59b6)

        #If user haven't provided a username, then we return error and ask to provide username.
        if member is None:
            embed.add_field(name="💢Error!💢", value="Please provide username or mention a person to ban.")
            return await ctx.channel.send(embed=embed)

	#If user have provided a username, then we try to ban that user and return feedback about proccess.
        try:
            await ctx.guild.ban(member, reason=reason)
            embed.add_field(name="⭐Success!⭐", value=f"Successfully baned `{member.name}` from `{ctx.guild.name}`.")
            await ctx.channel.send(embed=embed)
	    
        except discord.Forbidden:
            embed.add_field(name="💢Error!💢", value=f"Could not ban `{member.name}` from `{ctx.guild.name}`.")
            await ctx.channel.send(embed=embed)

    #Creating a kick command.
    #Setting rule to use command in guild only.
    #Doing a check for permissions "kick_members" required.	
    @commands.command(name="kick")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, *, member : discord.Member = None, reason = None):
        """Provide username or mention a person to kick from guild."""
        
        #Setting discord.Embed as embed and setting color.
        embed = discord.Embed(color = 0x9b59b6)

        #If user haven't provided a username, then we return error and ask to provide username.
        if member is None:
            embed.add_field(name="💢Error!💢", value="Please provide username or mention a person to kick.")
            return await ctx.channel.send(embed=embed)
	
        #If user have provided a username, then we try to kick that user and return feedback about proccess.
        try:
            await ctx.guild.kick(member, reason=reason)
            embed.add_feild(name="⭐Success!⭐", value=f"Successfully kicked `{member.name}` from `{ctx.guild.name}`.")
            await ctx.channel.send(embed=embed)
	    
        except discord.Forbidden:
            embed.add_field(name="💢Error!💢", value=f"Could not kick `{member.name}` from `{ctx.guild.name}`.")
            await ctx.channel.send(embed=embed)
            
    #Creating a kick command.
    #Setting rule to use command in guild only.
    #Doing a check for permissions "kick_members" required.
    @commands.command(name="Unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member = None):
        """Provide username example#1234 of person to unban him."""
        
        #Setting discord.Embed as embed and setting color.
        embed = discord.Embed(color = 0x9b59b6)
        
        #If user haven't provided a username, then we return error and ask to provide username.
        if member is None:
            embed.add_field(name="💢Error!💢", value="Please provide username or mention a person to kick.")
            return await ctx.channel.send(embed=embed)
            
        #If user have provided a username, then we try to unabn that user and return feedback about proccess.
        try:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = members.split("#")
            
            for ban_entry in banned_users:
                user = ban_entry.user
                
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    embed.add_field(name="⭐Success!⭐", value=f"Successfully removed `{member.name}` from ban list.")
                    await ctx.channel.send(embed=embed)
                    
        except (discord.Forbidden, discord.HTTPException):
            embed.add_field(name="💢Error!💢", value=f"Could not unban `{member.name}` from ban list.")
            await ctx.channel.send(embed=embed)
	
def setup(bot):
    bot.add_cog(Admin(bot))
