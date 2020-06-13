'''
Created on Jun 13, 2020

@author: leduke
'''
import time
from common.utils import getJSON
import discord
from discord.embeds import Embed

MATCH_REGULAR_IMAGE_URL = 'https://cdn.wikimg.net/en/splatoonwiki/images/archive/4/4c/20180326120211%21Mode_Icon_Regular_Battle_2.png'


def get_full_splatoon2_url(local_url):
    return "https://splatoon2.ink/assets/splatnet" + local_url


def get_stage_name(stage_id, translations):
    return translations['stages'][stage_id]['name']


async def command_maps(ctx, translations, offset=0):
    current_time = int(time.mktime(time.localtime()))
    data = getJSON("https://splatoon2.ink/data/schedules.json")
    trfWar = data['regular']
    ranked = data['gachi']
    league = data['league']
    theString = ''

    if offset == 0:
        theString = "Current Splatoon 2 Maps"
    elif offset == 1:
        theString = "Upcoming Splatoon 2 Maps"

    match_name = translations['game_modes']['regular']['name']
    theString = theString + "```{}:\n".format(match_name)

    mapA = trfWar[offset]['stage_a']
    mapA_name = get_stage_name(mapA['id'], translations)
    mapA_url = get_full_splatoon2_url(mapA['image'])
    mapB = trfWar[offset]['stage_b']
    mapB_name = get_stage_name(mapB['id'], translations)
    mapB_url = get_full_splatoon2_url(mapB['image'])
    end_time = trfWar[offset]['end_time']
    theString = theString + '{:22}'.format(mapA_name) + '\t' + mapB_name + '\n'

    timeRemaining = end_time - current_time
    timeRemaining = timeRemaining % 86400
    hours = int(timeRemaining / 3600)
    timeRemaining = timeRemaining % 3600
    minutes = int(timeRemaining / 60)

    if offset == 0:
        theString = theString + 'Time Remaining: '    
    elif offset >= 1:
        hours = hours - 2
        theString = theString + 'Time Until Map Rotation: '

    embed = Embed(title=match_name,
                  description="Temps restant : {} heures et {} minutes".format(hours, minutes),
                  color=discord.Color.default())
    embed.set_thumbnail(url=MATCH_REGULAR_IMAGE_URL)
    await ctx.send(embed=embed)

    embed = Embed(title=mapA_name, color=discord.Color.blue())
    embed.set_thumbnail(url=MATCH_REGULAR_IMAGE_URL)
    embed.set_image(url=mapA_url)
    await ctx.send(embed=embed)
    
    embed = Embed(title=mapB_name, color=discord.Color.blue())
    embed.set_thumbnail(url=MATCH_REGULAR_IMAGE_URL)
    embed.set_image(url=mapB_url)
    await ctx.send(embed=embed)


# 
#     match_name = translations['game_modes']['gachi']['name']
#     theString = theString + "\n{}: ".format(match_name)
# 
#     mapA = ranked[offset]['stage_a']
#     mapA_name = get_stage_name(mapA['id'])
#     mapB = ranked[offset]['stage_b']
#     mapB_name = get_stage_name(mapB['id'])
#     game = ranked[offset]['rule']
#     game_name = translations['rules'][game['key']]['name']
# 
#     theString = theString + game_name + '\n' + '{:22}'.format(mapA_name) + '\t' + mapB_name + '\n'
# 
#     match_name = translations['game_modes']['league']['name']
#     theString = theString + "\n{}: ".format(match_name)
#     
#     mapA = league[offset]['stage_a']
#     mapA_name = get_stage_name(mapA['id'])
#     mapB = league[offset]['stage_b']
#     mapB_name = get_stage_name(mapB['id'])
#     game = league[offset]['rule']
#     game_name = translations['rules'][game['key']]['name']
