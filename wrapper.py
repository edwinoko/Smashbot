'''
This file is a layer that connects the different function files with the bot. The reason this was done is to make the bot 
non reliant on any bot framework. 
'''


# this function is responsible for making sure that all the data has been scraped and putten in the raw_data directory
from crawler.data_crawler import get_data
from commands.frame_data_commands import *


def startup():
    data = get_data()
    # get all the smashframedata

    update = 'smash frame data has been loaded'
    
    return update

def handle_command(command):

    if command.startswith('!smash'):

        print('this is a smash command')

        answer = smash_command(command)

    return answer

def smash_command(command):

    # remove smash keyword from string
    # partition splits a string on the first separator

    if '|' in command:

        try:
            split_up_command = command.partition(' ')[2]

            command_parameters = split_up_command.split('|')

            if len(command) > 2:

                answer = get_frame_data(command_parameters[0],command_parameters[1])

                return answer
        except:
            print('this was not a request for framedata')

    if command.endswith('pickmycharacter'):

        answer = get_random_character()

    if 'vs' in command.lower():
        
        try:
            character = command.lower().replace('!smash','').strip().split('vs')
            matchup = get_matchup(character[0], character[1])
            return matchup
        except Exception as e:
            print('i think something went wrong'+str(e))

        #return answer

    answer = 'you might have made a typo or i dont know this command yet. Please feel free to let edwinoko know that you saw this'
    
    return answer
  
#smash_command('!smash Banjo & Kazooie | Jab 1')