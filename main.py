import discord
import os

client = discord.Client()

TOKEN = os.getenv('TOKEN')

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startwith('$smash'):
    await message.channel.send('we smashin bro')
  await client.process_commands(message)

client.run(TOKEN)