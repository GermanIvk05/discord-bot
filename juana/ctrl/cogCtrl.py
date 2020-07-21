#!/usr/bin/python3

import os
import discord
from discord.ext import commands
from juana.ctrl import logCtrl

class command:
	
	def load_cogs():
		"""Loading all modules at the start of bot"""
		
		bot = commands.Bot(command_prefix="!")
		logger = logCtrl.commands()
		
		for filename in os.listdir("./juana/cogs/"):
			if filename.endswith(".py"):
				bot.load_extension(f"juana.cogs.{filename[:-3]}")
				
#	def load_cog(module):
#		"""Loads a module"""
#		
#		self.logger("[*] Trying to load a module....")
#		
#		try:
#			self.bot.load_extension(f".juana.cogs.{module}")
#			
#		except Exception:
#			self.logger("[-] Couldn't load a module....")
#			return False
#			
#		else:
#			self.logger("[+] Module was successfully loaded.")
#			return True
#		
#		
#	def unload(module):
#		"""Unloads a module"""
#		
#		self.logger("[*] Trying to unload a module....")
#		
#		try:
#			self.bot.unload_extension(f".juana.cogs.{module}")
#			
#		except Exception:
#			self.logger("[-] Couldn't unload a module....")
#			return False
#			
#		else:
#			self.logger("[+] Module was successfully unloaded.")
#			return True
#			
#	def reload(module):
		
		
