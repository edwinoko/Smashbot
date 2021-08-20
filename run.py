import discord
import os

client = discord.Client()

TOKEN = os.getenv('TOKEN')

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.content.startwith('$smash'):
    await message.channel.send('we smashin bro')

  if message.content.startswith('$hello'):
    await message.channel.send("Hello!")

  if message.content.startswith("shrug"):
    await message.channel.send('¯\_(ツ)_/¯')
  
  if message.author == client.user:
    return
client.run(TOKEN)