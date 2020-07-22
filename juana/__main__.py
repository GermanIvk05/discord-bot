#!/usr/bin/python3

import os
from sys import argv
from os import environ
from dotenv import load_dotenv
from juana.__init__ import Juana


def print_usage():
	print("""Usage:
	Juana -h, --help    Shows this message.
	
	DISCORD_CHANNEL     should be environment variables.
	DISCORD_TOKEN       should be environment variables.
	DATABASE            should be environment variables.
	
	They can be placed in a `.env` file.
	The database will be created if it does not exist.
	""")
		
def main():  # If called by entrypoint
	if '--help' in argv or '-h' in argv:
		print_usage()
		exit()
        
	load_dotenv()
        
	errors = []
	if not environ.get('DISCORD_TOKEN'):
		errors.append('No DISCORD_TOKEN found in environment variables.')
		
	if not environ.get('DISCORD_CHANNEL'):
		errors.append('No DISCORD_CHANNEL found in environment variables.')

	if not environ.get('DATABASE'):
		errors.append('No DATABASE found in environment variables.')
		
	if errors:
		for error in errors:
			print(f"Error: {error}")
		exit(1)
        
	bot = Juana(environ['DISCORD_CHANNEL'], environ['DISCORD_TOKEN'], environ['DATABASE'])
				
	bot.run()
        
if __name__ == '__main__':
	main()
