#!/usr/bin/python3

from setuptools import setup

setup(
	name='juana',
	version='1.0.0',
	description='Advanced discord chat bot that uses AIML artificial intelligence.',
	long_description="See https://github.com/GermanIvk05/Discord-Bot",
	url='https://github.com/GermanIvk05/Discord-Bot', 
	author="GermanIvk05",
	author_email="germanIvk90@gmail.com",
	license='MIT License',
	scripts=['bin/juana'],
	pakages=['juana'],
	entry_points={
		'console_scripts': [
			'juana = juana.__main__:main',
		],
	},
	package_data={
		'juana': [
			'std-startup.xml',
	  		'aiml/alice/*.aiml',
	  		'aiml/custom/*.aiml',
	  		'cogs/*.py'
	  		],
	  	},
	zip_safe=False,
	install_requires=[
	  	'aiohttp==3.6.2',
	  	'discord.py == 1.3.3',
	  	'python-aiml==0.9.3',
	  	'websockets==8.1',
	  	'python-dotenv==0.14.0',
	],
	python_requires='>=3.7',
)
