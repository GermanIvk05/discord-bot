#!/usr/bin/python3

import os
import aiml
import sqlite3
import logging
import discord
import pkg_resources
from sys import exit
from discord.ext import commands
from datetime import datetime, timedelta
from signal import signal, SIGINT, SIGTERM


class Juana:
	
	STARTUP_FILE = "std-startup.xml"
	SQL_SCHEMA = [
		'CREATE TABLE IF NOT EXISTS chat_log (time, server_name, user_id, message, response)',
		'CREATE TABLE IF NOT EXISTS users (id, name, first_seen)',
		'CREATE TABLE IF NOT EXISTS servers (id, name, first_seen)',
	]
	
	def print_log(self, text, level):
		LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
		
		logging.getLogger('discord').setLevel(logging.INFO)
		logging.getLogger('discord.http').setLevel(logging.WARNING)
        
		logging.basicConfig(filename="juana.log",
							level = logging.INFO,
							format = LOG_FORMAT,
							filemode = 'w')
								
		logger = logging.getLogger(__name__)
		ch = logging.StreamHandler()
		ch.setLevel(logging.INFO)
			
		if logger.hasHandlers():
			logger.handlers.clear()
				
		logger.addHandler(ch)
		
		if level == "d" or level == "D":
			logger.debug(text)			
		elif level == "i" or level == "I":
			logger.info(text)			
		elif level == "w" or level == "W":
			logger.warning(text)		
		elif level == "e" or level == "E":
			logger.error(text)		
		elif level == "c" or level == "C":
			logger.critical(text)			
		else:
			return
	
	def exit_handler(self, signal_received, frame):
		self.print_log(f"[*] Signal received ({signal_received})...Exiting.", "i")
		exit()
		
	def __init__(self, channel_name, bot_token, database):
		"""
		Initialize the bot using the Discord token and channel name to chat in.
		
		:param channel_name: Only chats in this channel. No hashtag included.
		:param bot_token: Full secret bot token
		:param database: Path for sqlite file to use
		"""
        
		# Store configuration values
		self.channel_name = channel_name
		self.prefix = "!"
		self.token = bot_token
		self.database = database
		self.message_count = 0
		self.last_reset_time = datetime.now()
        
		self.print_log("[*] Setting up signal handlers...", "i")
		signal(SIGINT, self.exit_handler)
		signal(SIGTERM, self.exit_handler)
		
		# Setup database
		self.print_log("[*] Initializing database...", "i")
		self.db = sqlite3.connect(self.database)
		self.cursor = self.db.cursor()
		self.setup_database_schema()
		self.print_log("[+] Database initialized", "i")
		
		# Load AIML kernel
		self.print_log("[*] Initializing AIML kernel...", "i")
		start_time = datetime.now()
		self.aiml_kernel = aiml.Kernel()
		self.setup_aiml()
		end_time = datetime.now()
		self.print_log(f"[+] Done initializing AIML kernel. Took {end_time - start_time}", "i")
		
		# Set up Discord
		self.print_log("[*] Initializing Discord bot...", "i")
		self.discord_bot = discord.AutoShardedClient()
		self.setup_discord_events()
		self.print_log("[+] Done initializing Discord bot.", "i")
		self.print_log("[+] Exiting __init__ function.", "i")
		
	
	def setup_database_schema(self):
		for sql_statement in self.SQL_SCHEMA:
			self.cursor.execute(sql_statement)
		self.db.commit()
		
	def setup_aiml(self):
		intial_dir = os.getcwd()
		os.chdir(pkg_resources.resource_filename(__name__, ""))
		startup_filename = pkg_resources.resource_filename(__name__, self.STARTUP_FILE)
		self.aiml_kernel.setBotPredicate("name", "Juana")
		self.aiml_kernel.learn(startup_filename)
		self.aiml_kernel.respond("LOAD AIML B")
		os.chdir(intial_dir)
		
	async def reset(self, message):
		"""
		Allow users to trigger a Juana reset up to once per hour. This can help when the bot quits responding.
		:return:
		"""
		
		now = datetime.now()
		
		if datetime.now() - self.last_reset_time > timedelta(hours-1):
			self.last_reset_time = now
			await message.channel.send("Resetting my brain...")
			self.aiml_kernel.resetBrain()
			self.setup_aiml()
			
		else:
			await message.channel.send(f'Sorry, I can only reset once per hour and I was last reset on {self.last_reset_time} UTC')
			
	def setup_discord_events(self):
		"""
		This method defines all of the bot command nad hook callbacks
		:return:
		"""
		
		self.print_log("[+] Setting up Discord events", "i")
		
		@self.discord_bot.event
		async def on_ready():
			self.print_log("[+] Bot on_ready even fired. Connected to Discord", "i")
			self.print_log("[*] Name: {}".format(self.discord_bot.user.name), "i")
			self.print_log("[*] ID: {}".format(self.discord_bot.user.id), "i")
		
		@self.discord_bot.event
		async def on_message(message):
			
			self.message_count += 1
			
			if message.author.bot or str(message.channel) != self.channel_name:
				return
				
			if message.content is None:
				self.print_log("[-] Empty message received... Ignoring.", "w")
				return
				
			# Clean out the message to prevent issues
			text = message.content
			
			for ch in ['/', "'", ".", "\\", "(", ")", '"', '\n', '@', '<', '>']:
				text = text.replace(ch, '')
				
			try:
				aiml_response = self.aiml_kernel.respond(text)
				aiml_response = aiml_response.replace("://", "")
				aiml_response = aiml_response.replace("@", "")
				db_response = "@%s %s" % (message.author.name, aiml_response)
				aiml_response = "%s %s" % (message.author.mention, aiml_response)
				
				if len(aiml_response) > 1800:
					aiml_response = aiml_response[0:1800]
					
				now = datetime.now()
				self.insert_chat_log(now, message, db_response)
				
				await message.channel.send(aiml_response)
				
			except discord.HTTPException as e:
				self.print_log("[-] Discord HTTP Error: %s" % e, "e")
			except Exception as e:
				self.print_log("[-] General Error: %s" % e, "e")
				
	def run(self):
		self.print_log("[*] Now calling run()", "i")
		self.discord_bot.run(self.token)
		self.print_log("[*] Bot finished running.", "i")
		
	def insert_chat_log(self, now, message, aiml_response):
		self.cursor.execute('INSERT INTO chat_log VALUES (?, ?, ?, ?, ?)',
							(now.isoformat(), message.guild.id, message.author.id,
							str(message.content), aiml_response))
							
		# Add user if necessary
		self.cursor.execute('SELECT id FROM users WHERE id=?', (message.author.id,))
		
		if not self.cursor.fetchone():
			self.cursor.execute('INSERT INTO users VALUES (?, ?, ?)',
								(message.author.id, message.author.name, datetime.now().isoformat()))
								
		# Add server if necessary
		self.cursor.execute('SELECT id FROM servers WHERE id=?', (message.guild.id,))
		
		if not self.cursor.fetchone():
			self.cursor.execute('INSERT INTO servers VALUES (?, ?, ?)',
								(message.guild.id, message.guild.name, datetime.now().isoformat()))
								
		self.db.commit()
