'''
Created on Jun 12, 2020

@author: leduke
'''
from discord.ext import commands
import json
import sys
from common.utils import getJSON
from splatoon2.maps import command_maps

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!', description=description)
token = ''
commands = ''
language = 'en'
configData = None
splatoon2_translations = {}

def loadConfig(firstRun=0):
    global token, commands, language
    try:
        with open('./discordbot.json', 'r') as json_config:
            configData = json.load(json_config)

        token = configData['token']
        commands = configData['commands']
        language = configData['language']

        print('Config Loaded')
    except:
        print('Failed to load config')
        quit(1)


def loadTranslations():
    global splatoon2_translations
    splatoon2_translations = getJSON("https://splatoon2.ink/data/locale/" + language + ".json")


@bot.command()
async def maps(ctx, offset=0):
    await command_maps(ctx, splatoon2_translations, offset)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

#Setup
# sys.stdout = open('./discordbot.log', 'a')
print('**********NEW SESSION**********')
loadConfig()
loadTranslations()

print('Logging into discord')
bot.run(token)
