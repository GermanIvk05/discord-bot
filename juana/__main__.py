#!/usr/bin/python3

import os
from sys import argv
from os import environ
from dotenv import load_dotenv
from juana.__init__ import Juana


def print_banner():
    print("""
          JJJJJJJJJJJ                                                                     
          J:::::::::J                                                                     
          J:::::::::J                                                                     
          JJ:::::::JJ                                                                     
            J:::::Juuuuuu    uuuuuu    aaaaaaaaaaaaa  nnnn  nnnnnnnn      aaaaaaaaaaaaa   
            J:::::Ju::::u    u::::u    a::::::::::::a n:::nn::::::::nn    a::::::::::::a  
            J:::::Ju::::u    u::::u    aaaaaaaaa:::::an::::::::::::::nn   aaaaaaaaa:::::a 
            J:::::ju::::u    u::::u             a::::ann:::::::::::::::n           a::::a 
            J:::::Ju::::u    u::::u      aaaaaaa:::::a  n:::::nnnn:::::n    aaaaaaa:::::a 
JJJJJJJ     J:::::Ju::::u    u::::u    aa::::::::::::a  n::::n    n::::n  aa::::::::::::a 
J:::::J     J:::::Ju::::u    u::::u   a::::aaaa::::::a  n::::n    n::::n a::::aaaa::::::a 
J::::::J   J::::::Ju:::::uuuu:::::u  a::::a    a:::::a  n::::n    n::::na::::a    a:::::a 
J:::::::JJJ:::::::Ju:::::::::::::::uua::::a    a:::::a  n::::n    n::::na::::a    a:::::a 
 JJ:::::::::::::JJ  u:::::::::::::::ua:::::aaaa::::::a  n::::n    n::::na:::::aaaa::::::a 
   JJ:::::::::JJ     uu::::::::uu:::u a::::::::::aa:::a n::::n    n::::n a::::::::::aa:::a
     JJJJJJJJJ         uuuuuuuu  uuuu  aaaaaaaaaa  aaaa nnnnnn    nnnnnn  aaaaaaaaaa  aaaa
""")

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
