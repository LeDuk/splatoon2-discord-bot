#!/usr/bin/python3

import discord
import asyncio
import sys
import json
import time
import urllib
import urllib.request
import datetime
import calendar

client = discord.Client()
token = ''
commands = ''
configData = None

def loadConfig(firstRun=0):
	global token, commands
	try:
		with open('./discordbot.json', 'r') as json_config:
			configData = json.load(json_config)

		token = configData['token']
		commands = configData['commands']

		print('Config Loaded')
	except:
		print('Failed to load config')
		quit(1)

def getJSON(url):
	req = urllib.request.Request(url, headers={ 'User-Agent' : 'Magic!' })
	response = urllib.request.urlopen(req)
	data = json.loads(response.read().decode())
	return data

async def spParser(message):
	theTime = int(time.mktime(time.gmtime()))
	data = getJSON("https://splatoon2.ink/data/merchandises.json")
	gear = data['merchandises']
	theString = ''

	theString = 'Current SplatNet Gear:\n```'

	for i in gear:
		skill = i['skill']
		equip = i['gear']
		price = i['price']
		end = i['end_time']
		eqName = equip['name']
		eqBrand = equip['brand']['name']
		commonSub = equip['brand']['frequent_skill']['name']
		eqKind = equip['kind']
		slots = equip['rarity'] + 1

		timeRemaining = end - theTime
		timeRemaining = timeRemaining % 86400
		hours = int(timeRemaining / 3600)
		timeRemaining = timeRemaining % 3600
		minutes = int(timeRemaining / 60)

		theString = theString + eqName + ' : ' + eqBrand + '\n'
		theString = theString + '    Skill      : ' + str(skill['name']) + '\n'
		theString = theString + '    Common Sub : ' + str(commonSub) + '\n'
		theString = theString + '    Subs       : ' + str(slots) + '\n'
		theString = theString + '    Type       : ' + eqKind + '\n'
		theString = theString + '    Price      : ' + str(price) + '\n'
		theString = theString + '    Time Left  : ' + str(hours) + ' Hours and ' + str(minutes) + ' minutes\n\n'

	theString = theString + '```'
	await client.send_message(message.channel, theString)


async def srParser(message, getNext=0):
	theTime = int(time.mktime(time.gmtime()))
	data = getJSON("https://splatoon2.ink/data/coop-schedules.json")
	currentSR = data['details']
	gotData = 0
	start = 0
	end = 0
	theString = ""	

	if getNext == 0:
		theString = theString + "Current Salmon Run:\n```"
	else:
		theString = theString + "Upcoming Salmon Run:\n```"

	for i in currentSR:
		gotData = 0
		start = i['start_time']
		end = i['end_time']
		map = i['stage']
		weaps = i['weapons']

		if start <= theTime and theTime <= end:
			gotData = 1

		if (gotData == 1 and getNext == 0) or (gotData == 0 and getNext == 1):
			theString = theString + "Map: " + map['name'] + '\nWeapons:\n'
			for j in i['weapons']:
				try:
					weap = j['weapon']
				except:
					weap = j['coop_special_weapon']
				theString = theString + '\t' + weap['name'] + '\n'
			break

		elif gotData == 1 and getNext == 1:
			gotData = 0
			continue

	theString = theString + '\n'

	if gotData == 0 and getNext == 0:
		theString = theString + 'No SR currently running```'
		await client.send_message(message.channel, theString)
		return
	elif getNext == 1:
		timeRemaining = start - theTime
		theString = theString + '```Time Until This Rotation : '
	else:
		timeRemaining = end - theTime
		theString = theString + '```Time remaining : '

	days = int(timeRemaining / 86400)
	timeRemaining = timeRemaining % 86400
	hours = int(timeRemaining / 3600)
	timeRemaining = timeRemaining % 3600
	minutes = int(timeRemaining / 60)

	theString = theString + str(days) + ' Days, ' + str(hours) + ' Hours, and ' + str(minutes) + ' minutes'

	await client.send_message(message.channel, theString)

@client.event
async def on_ready():
	print('Logged in as,', client.user.name, client.user.id)
	print('------')
	await client.change_presence(activity=discord.Game(name="Use !help for directions!", type=0))

@client.event
async def on_server_join(server):
	print("I joined server: " + server.name)

@client.event
async def on_message(message):
#	if message.server == None:
#		return
	if message.author.name == client.user.name:
		return
	elif message.content.startswith('!alive'):
		text = "Hey " + message.author.name + ", I'm alive so shut the fuck up! :japanese_goblin:"
		await client.send_message(message.channel, text)
	elif message.content.startswith('!github'):
		await client.send_message(message.channel, 'Here is my github page! : https://github.com/Jetsurf/splatoon2-discord-bot')
	elif message.content.startswith('!commands') or message.content.startswith('!help'):
		theString = ''
		with open(commands, 'r') as f:
			for line in f:
				theString = theString + line
		await client.send_message(message.channel, theString)
	elif message.content.startswith('!currentmaps'):
		await maps(message)
	elif 'nextmaps' in message.content and '!' in message.content:
		await maps(message, offset=min(11, message.content.count('next')))
	elif message.content.startswith('!currentsr'):
		await srParser(message)
	elif message.content.startswith('!splatnetgear'):
		await spParser(message)
	elif message.content.startswith('!nextsr'):
		await srParser(message, 1)
	
#Setup
sys.stdout = open('./discordbot.log', 'a')
print('**********NEW SESSION**********')
loadConfig()

print('Logging into discord')

client.run(token)

