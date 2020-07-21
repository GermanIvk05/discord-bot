#!/usr/bin/python3

import random
import aiohttp
import asyncio
import discord
from discord.ext import commands

class TicTacToe:

    def __init__(self):
        #Creating a list of emoji from 1 to 9 (it will be a square selection).
        self.board = [[":one:", ":two:", ":three:"],[":four:", ":five:", ":six:"], [":seven:", ":eight:", ":nine:"]]
        
    #Assembling emoji the right way.
    def printStr(self):
        basestr = ""
        for i in self.board:
            for j in i:
                basestr += j
            basestr += "\n"
        return basestr
    
    #Win condition check.    
    def checkWin(self, player):
    
        #Right diaognal check
        if self.board[0][2] == player and self.board[1][1] == player and self.board[2][0] == player:
            return True
        
        #Left diaognal check.
        elif self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] ==player:
            return True
        
        #Vertical check
        for i in range(3):
            if self.board[0][i] == player and self.board[1][i] == player and self.board[2][i] == player:
                return True
                
        #Horizontal check.
        for i in range(3):
            if self.board[i][0] == player and self.board[i][1] == player and self.board[i][2] == player:
                return True
                
        #Executed if no check were passed.
        return False
    
    #Checking the move.    
    def checkMove(self, cell):
        row, index = self.cellConvert(cell)
        value = self.board[row][index]
        
        if value == ":o:":
            return False
            
        elif value == ":x:":
            return False
            
        else:
            return True
            
    #Cell converter.
    def cellConvert(self, cell):
    
        if cell <= 3:
            con = (0, cell-1)
            return con
            
        elif cell > 3 and cell <= 6:
            con = (1, cell-4)
            return con
        
        elif cell > 6 and cell <= 9:
            con = (2, cell-7)
            return con
            
        return
        
    #Play move
    def playMove(self, cell, player):
        row, index = self.cellConvert(cell)
        self.board[row][index] = player
        
    #Check if board is full
    def isFull(self):
        count = 0
        for i in self.board:
            for j in i:
                if j == ":o:" or j == ":x:":
                    count += 1
                
                else:
                    pass
        
        if count < 9:
            return False
        
        return True
        
class Games(commands.Cog):
    """contains commands to have some fun with your pals."""
    
    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()
        self.boardEmoji = ["1️⃣", "2️⃣", "3️⃣" ,"4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    
    #Returning True or False depends on win or loss.   
    def _parseWin(self, member, automation):
        if automation == member:
            return None
            
        elif member == "rock" or member == "Rock":
            return True if automation == "scissor" else False
                        
        elif member == "paper" or member == "Paper":
            return True if automation == "rock" else False
                        
        else:
            return True if autonation == "paper" else False
            
    #Creating a Tic Tac Toe command.
    #Setting rule to use in guild only.
    @commands.command(name="tictactoe", aliases=["ttc"])
    @commands.guild_only()
    async def tictactoe(self, ctx, member : discord.Member = None):
        """Play a game of Tic Tac Toe with your friend"""
        
        #Setting discord.Embed as embed and setting color.
        embed = discord.Embed(color = 0x9b59b6)
        
        #Checking if member arg was passed in.
        if member is None:
            embed.add_field(name="💢Error!💢", value="Please specify username or mention, whom you want to play Tic Tac Toe with")
            return await ctx.channel.send(embed=embed)
        
        #Checking if member arg is a bot.    
        if member.bot:
            embed.add_field(name="💢Error!💢", value="You can't play with bots.")
            return await ctx.channel.send(embed=embed)
            
        #Checking if member arg is ourselfs.    
        if member == ctx.author:
            embed.add_field(name="💢Error!💢", value="You can't challenge yourself!")
            return await ctx.channel.send(embed=embed)
            
        #Cheking if game session in this guild is running.    
        if ctx.guild.id in self.sessions:
            embed.add_field(name="💢Error!💢", value="A game is already being played in this server.")
            return await ctx.channel.send(embed=embed)
        
        #Adding guild id to sessions and poping challange msg + reactions    
        self.sessions.add(ctx.guild.id)
        embed.add_field(name="Tic Tac Toe Challange.", value=f"""{member.name}, you have been challenged by {ctx.author.name} to a round of Tic Tac Toe, will you accept the challenge? Reply `Y` for yes and `N` for no. This will terminate in `30 seconds`.""")
        embedMessage = await ctx.channel.send(member.mention, embed=embed)
        
        #Adding ractions to our message.
        await embedMessage.add_reaction("🇾")
        await embedMessage.add_reaction("🇳")
        
        #Checking channel, the right user and answer value
        def check(reaction, user):
            if ctx.channel == ctx.message.channel and user == member:
                if str(reaction.emoji) == "🇾" or str(reaction.emoji) == "🇳":
                    return True
                    
                return False
        
        #Waiting for reaction answer for 30sec, if no reaction was added return a msg.
        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
        
        except asyncio.TimeoutError:
            self.sessions.remove(ctx.guild.id)
            embed.clear_fields()
            embed.add_field(name="💢Error!💢", value=f"{member.mention} took too long to respond, terminating the challange.")
            return await ctx.channel.send(embed=embed)
        
        #Checking if the answer is 'yes'    
        if str(reaction.emoji) == "🇾":
            embedMessage.delete()
            winner = None
            player = (":x:", ctx.author)
            opp = (":o:", member)
            boardActual = TicTacToe()
            
            #Checking reacton from player.
            def playerReactCheck(reaction, user):
            
                #Checking if reaction is from right user.
                if user == player[1]:
                
                    #Checking the emoji, then cheking that move, if move is ok, do playMove.
                    if str(reaction.emoji) == "1️⃣":
                        if boardActual.checkMove(1):
                            boardActual.playMove(1, player[0])
                            return True
                            
                    elif str(reaction.emoji) == "2️⃣":
                        if boardActual.checkMove(2):
                            boardActual.playMove(2, player[0])
                            return True
                            
                    elif str(reaction.emoji) == "3️⃣":
                        if boardActual.checkMove(3):
                            boardActual.playMove(3, player[0])
                            return True
                            
                    elif str(reaction.emoji) == "4️⃣":
                        if boardActual.checkMove(4):
                            boardActual.playMove(4, player[0])
                            return True
                            
                    elif str(reaction.emoji) == "5️⃣":
                        if boardActual.checkMove(5):
                            boardActual.playMove(5, player[0])
                            return True
                            
                    elif str(reaction.emoji) == "6️⃣":
                        if boardActual.checkMove(6):
                            boardActual.playMove(6, player[0])
                            return True
                            
                    elif str(reaction.emoji) == "7️⃣":
                        if boardActual.checkMove(7):
                            boardActual.playMove(7, player[0])
                            return True
                            
                    elif str(reaction.emoji) == "8️⃣":
                        if boardActual.checkMove(8):
                            boardActual.playMove(8, player[0])
                            return True
                            
                    elif str(reaction.emoji) == "9️⃣":
                        if boardActual.checkMove(9):
                            boardActual.playMove(9, player[0])
                            return True
                                
                return False
            
            #Checking reaction from opp.         
            def oppReactCheck(reaction, user):
            
                #Checking if reaction is from right user.
                if user == opp[1]:
                
                    #Checking the emoji, then cheking that move, if move is ok, do playMove.
                    if str(reaction.emoji) == "1️⃣":
                        if boardActual.checkMove(1):
                            boardActual.playMove(1, opp[0])
                            return True
                            
                    elif str(reaction.emoji) == "2️⃣":
                        if boardActual.checkMove(2):
                            boardActual.playMove(2, opp[0])
                            return True
                            
                    elif str(reaction.emoji) == "3️⃣":
                        if boardActual.checkMove(3):
                            boardActual.playMove(3, opp[0])
                            return True
                            
                    elif str(reaction.emoji) == "4️⃣":
                        if boardActual.checkMove(4):
                            boardActual.playMove(4, opp[0])
                            return True
                            
                    elif str(reaction.emoji) == "5️⃣":
                        if boardActual.checkMove(5):
                            boardActual.playMove(5, opp[0])
                            return True
                            
                    elif str(reaction.emoji) == "6️⃣":
                        if boardActual.checkMove(6):
                            boardActual.playMove(6, opp[0])
                            return True
                            
                    elif str(reaction.emoji) == "7️⃣":
                        if boardActual.checkMove(7):
                            boardActual.playMove(7, opp[0])
                            return True
                            
                    elif str(reaction.emoji) == "8️⃣":
                        if boardActual.checkMove(8):
                            boardActual.playMove(8, opp[0])
                            return True
                            
                    elif str(reaction.emoji) == "9️⃣":
                        if boardActual.checkMove(9):
                            boardActual.playMove(9, opp[0])
                            return True
                                
                return False

            
            #Creating a while loop    
            while True:
            
                #Checking if the board is full
                if boardActual.isFull():
                    break
                
                #Sending messages and the board
                part1 = await ctx.channel.send("**The Board**")
                part2 = await ctx.channel.send(boardActual.printStr())
                playerMove = await ctx.channel.send(f"{player[1].mention}, it's your turn! You have 30 seconds to play a move, or you will lose.")
 
                #Adding reactions
                for i in self.boardEmoji:
                    await part2.add_reaction(i)
                    
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=playerReactCheck)
                    
                except asyncio.TimeoutError:
                    await ctx.channel.send(f"{player[1].mention} took too long to play a move.")
                    winner = opp
                    break
                
                #Removing previos messages    
                await part1.delete()
                await part2.delete()
                await playerMove.delete()
                
                #Checking for win
                if boardActual.checkWin(player[0]):
                    winner = player
                    break
                
                #Checking if the board is full    
                if boardActual.isFull():
                    break
                
                #Sending messages and the board    
                part1 = await ctx.channel.send("**The Board**")
                part2 = await ctx.channel.send(boardActual.printStr())
                playerMove = await ctx.channel.send(f"{opp[1].mention}, it's your turn! You have 30 seconds to play a move, or you will lose.")
                    
                #Adding reactions
                for i in self.boardEmoji:
                    await part2.add_reaction(i)
                    
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=oppReactCheck)
                    
                except asyncio.TimeoutError:
                    await ctx.channel.send(f"{opp[1].mention} took too long to play a move.")
                    winner = player
                    break
                
                #Removing previos messages    
                await part1.delete()
                await part2.delete()
                await playerMove.delete()
                
                #cheking for win
                if boardActual.checkWin(opp[0]):
                    winner = opp
                    break
            
            #Checking if winner is none, if so ... it's a Draw (TIE)        
            if winner is None:
                part1 = await ctx.channel.send("**The Board**")
                part2 = await ctx.channel.send(boardActual.printStr())
                await ctx.channel.send("There was no winner, that means it's a TIE, and that means you BOTH WIN!")
                
            else:
                part1 = await ctx.channel.send("**The Board**")
                part2 = await ctx.channel.send(boardActual.printStr())  
                await ctx.channel.send(f"The winner is {winner[1].mention}!")
                
        else:
            await ctx.channel.send(f"Challenge declined by {user.mention}.")
        self.sessions.remove(ctx.guild.id)
    
    
    #Creating a Rock Paper Scissors command.
    #Setting rule to use in guild only.    
    @commands.command(name="rps")
    @commands.guild_only()
    async def rps(self, ctx, move : str = None):
        """Play a turn of rock paper scisors with me.
        Valid moves are: rock, paper, scissors!
        """
        
        #Setting discord.Embed as embed and setting color.
        #Also creating move tuple.
        embed = discord.Embed(color=0x9b59b6)
        movesTuple = ("rock", "paper", "scissors")
        
        #Cheking if move is none.
        if move is None:
            embed.add_field(name="💢Error!💢", value="Please specify your move!")
            return await ctx.channel.send(embed=embed)
            
        #Checking if move is not in move tuple.
        elif not move.lower() in movesTuple:
            embed.add_field(name="💢Error!💢", value="Invalid move, only `rock`, `paper` and `scissor`.")
            return await ctx.channel.send(embed=embed)
            
        rand = random.choice(movesTuple)
        res = await self.bot.loop.run_in_executor(None, self._parseWin, move.lower(), rand)
        
        #Checking the results.
        if res is None:
            embed.add_field(name="⭐It's a TIE!⭐", value=f"Result: `{move} == {rand}`.")
            return await ctx.channel.send(embed=embed)
        
        if res:
            embed.add_field(name="💢I lost!!!💢", value=f"Result: `{move.lower()} > {rand}`.")
            return await ctx.channel.send(embed=embed)
            
        embed.add_field(name="⭐I won this one.⭐", value=f"Result: `{rand} > {move.lower()}`")
        await ctx.channel.send(embed=embed)
        
    #Creating chucknorris command.
    #Setting rule to use in guild only.
    @commands.command(name="chuck", aliases=["chucknorris", "norris"])
    @commands.guild_only()
    async def _chunkNorris(self, ctx):
        """Get a random Chuck Norris joke."""
        
        #Getting chuck norris joke through json
        async with aiohttp.ClientSession() as sess:
            async with sess.get("http://api.icndb.com/jokes/random", params={"escape": "javascript"}) as resp:
                joke = await resp.json()
        
        #Setting discord.Embed as embed and setting color.        
        embed = discord.Embed(title="Chuck Norris", description=joke["value"]["joke"], color=0x9b59b6)
        embed.set_thumbnail(url="https://ih1.redbubble.net/image.415810949.3572/flat,550x550,075,f.u3.jpg")
        await ctx.channel.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Games(bot))
