'''
This file is a layer that connects the different function files with the bot. The reason this was done is to make the bot 
non reliant on any bot framework. 
'''

# this function is responsible for making sure that all the data has been scraped and putten in the raw_data directory

from random import randint
import discord
from crawler.data_crawler import get_data
from commands.frame_data_commands import *


# get all the smashframedata
def startup():
    get_data()
    update = 'smash frame data has been loaded'
    return update

def rating(command):
    removed_command = command.split(' ')
    del removed_command[0]
    if type(removed_command) is str:
        text = (removed_command)
    else:
        text = " ".join(removed_command)   
    number = randint(1,100)
    answer = 'I rate '+text+' '+str(number)+'%'
    return str(answer)
     
def pick_random_character():
    answer = get_random_character()
    title = 'Random Character Selection'
    footer = 'Provided by the Smash Gods. May rng forever be in your favour'
    result = embed_answer(answer, title, footer)
    return result


# remove smash keyword from string
# partition splits a string on the first separator

def frame_data(command):

    split_up_command = command.partition(' ')[2]
    command_parameters = split_up_command.split('|')
    answer = get_frame_data(command_parameters[0],command_parameters[1])
    title = command_parameters[0].strip()+'\'s '+command_parameters[1].strip()
    footer='Data was collected from ultimateframedata.com'

    answer = embed_answer(answer, title, footer)
    
    return answer

def matchup(command):
 
    character = command.lower().replace('!smash','').strip().split('vs')
    matchup = get_matchup(character[0], character[1])
    title='Matchup Analysis'
    footer='Data was collected from eventhubs.com/ssbu'
    answer = embed_answer(matchup, title, footer)
    return answer

def embed_answer(answer, title='', footer=''):
    embed = discord.Embed(
        title=title
    )
    if type(answer) is str:
        if 'http' in answer:
            embed.set_image(url=answer)
        else:
            print(answer)
            embed.add_field(name='-', value=answer, inline=False)
    
    elif type(answer) is list:
        for line in answer:
            if 'http' in line:
                embed.set_image(url=line)
            else:
                embed.add_field(name='-', value=line, inline=False)
    
    embed.set_footer(text=footer)

    return embed

  
#smash_command('!smash Banjo & Kazooie | Jab 1')