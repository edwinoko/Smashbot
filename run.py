from wrapper import *
from random_quotes.quote import get_random_quote
import os
import discord
from dotenv import load_dotenv

client = discord.Client()

load_dotenv()
#TOKEN = os.environ.get('DISCORD_TOKEN', None)
TOKEN = os.getenv('DISCORD_TOKEN')

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.content.startswith('$smash'):
    await message.channel.send('we smashin bro?!')
  
  if 'tuna steak' in message.content:
    await message.channel.send('fake news')

  if message.content.startswith('$hello'):
    await message.channel.send("Hello!")

  if message.content.startswith("shrug"):
    await message.channel.send('¯\_(ツ)_/¯')

  if message.content.startswith("!rate"):
    rate = rating(message.content)
    await message.channel.send(rate)  

# sends a random gamer quote
  if message.content.startswith("gg"):
    await message.channel.send(get_random_quote())

# random character selection
  if 'pickmycharacter' in message.content:
    answer = pick_random_character()
    await message.channel.send(embed=answer)

# get frame data of a character
  if message.content.startswith('!smash') and '|' in message.content:
    answer = frame_data(message.content)
    await message.channel.send(embed=answer)

# get matchup data of the character
  if message.content.startswith('!smash') and 'vs' in message.content:
    answer = matchup(message.content)
    await message.channel.send(embed=answer)

  if message.author == client.user:
    return
  
client.run(TOKEN)

