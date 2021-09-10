from wrapper import handle_command, smash_command
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
    rating = handle_command(message.content)
    await message.channel.send(rating)  

# sends a random gamer quote
  if message.content.startswith("gg"):
    await message.channel.send(get_random_quote())

# get frame data of a character
  if message.content.startswith('!smash'):
    list_of_lines = handle_command(message.content)
    # send string to the function to analyze the smash command.
    if type(list_of_lines) is list:
      for line in list_of_lines:
        await message.channel.send(line)
    if type(list_of_lines) is str:
      await message.channel.send(list_of_lines)

# random character selection
  if 'pickmycharacter' in message.content:
    answer = smash_command(message.content)
    await message.channel.send(answer)
 
  if message.author == client.user:
    return
  
client.run(TOKEN)

