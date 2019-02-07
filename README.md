# Splatoon 2 Map/SR/Splatnet bot
This bot was originally created at the following repo.
https://github.com/Jetsurf/jet-bot

It has been cut down from that version to allow Discord servers easy access
to get S2 Map/SR/Splatnet information right in their server!

## Installation
#Self Hosted
Requires https://github.com/Rapptz/discord.py discord python library to 
function.

Requires a Discord API application to be setup
https://discordapp.com/developers/applications/

Run the bot.py script.

#Easy Install
Use the following link to login to discord and add the bot to your server!
https://discordapp.com/oauth2/authorize?client_id=542882637883113492&permissions=2048&scope=bot

## Configuration
An example configuration file is given at discordbot.json.example.
This file needs to be completed and moved to discordbot.json.

## Use
Complete the discordbot.json config file with the necessary fields. 
Currently implemented commands are as follows:
 - !currentmaps : Displays the current Splatoon 2 Gamemodes/Maps
 - !nextmaps : Displays the upcoming Splatoon 2 Gamemodes/Maps
   (!nextnextmaps displays 2 map rotations from now, etc)
 - !currentsr : Displays the current Splatoon 2 Salmon Run Map/Weapons
 - !nextsr : Displays the next Splatoon 2 Salmon Run Map/Weapons
 - !splatnetgear : Gets all of the current gear for sale on SplatNet
 - !github : Displays my github link
