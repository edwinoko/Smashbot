#import
import json,  random
from pathlib import Path

# move framedata
def get_frame_data(character, move):
    character = character.strip().lower().replace(' ','_')
    move = move.strip().lower().replace(' ','_')

    cwd = str(Path.cwd())

    #import pdb; pdb.set_trace()

    f = open(cwd+'/smash_character_data/'+character+".json")

    character_data = json.load(f)
    
    try:
        data = character_data['moves'][move]
        answer = ['https://ultimateframedata.com/'+data['hitbox'], 
               'Startup frames : '+data['startup'],
               'Active frames : '+data['activeframes'],
               'this attack is '+data['advantage']+' on shield',
                data['notes']]

        return answer
    except KeyError:
        for key in character_data['moves'].keys():
            if move in key:
                data = character_data['moves'][key]
                answer = ['https://ultimateframedata.com/'+data['hitbox'], 
                    'Startup frames : '+data['startup'],
                    'Active frames : '+data['activeframes'],
                    'this attack is '+data['advantage']+' on shield',
                    data['notes']]
                return answer


def get_random_character():
    directory_in_str = str(Path.cwd())+'/smash_character_data'
    all_characters = []

    pathlist = Path(directory_in_str).glob('*.json')
    for path in pathlist:
     # because path is object not string
        path_in_str = str(path).split('/')[-1].replace('.json','').replace('_',' ')
        # print(path_in_str)
        all_characters.append(path_in_str)
    
    return random.choice(all_characters)

#
def get_matchup(character_one, character_two):
    #print(character_one, character_two)
    directory_in_str = str(Path.cwd())+'/matchup_data'
    pathlist = Path(directory_in_str).glob('*.json')
    answers = []
    for path in pathlist:
     # because path is object not string
        character= str(path).split('/')[-1].replace('.json','').lower().strip().replace(' ','-').replace('.','')
        character_one = character_one.strip().replace(' ','-')
        if character == character_one:

            # Opening JSON file
            f = open(path,)
            data = json.load(f)
            f.close()
            #print(character_one.lower().strip().replace(' ','-'),character_two.lower().strip().replace(' ','-'))

            matchup_number = data[character_one.lower().strip().replace(' ','-')][character_two.lower().strip().replace(' ','-')]
            #print(character_one.lower().strip().replace(' ','-'),character_two.lower().strip().replace(' ','-'))
            answer = 'The '+character_one+' vs '+character_two+' is '+str(matchup_number)+ ' out of 10 matchup.'

            if float(matchup_number) < 4.8:
                answers = [answer, 'You are in for a rough matchup. Good luck!']

            if float(matchup_number) > 4.8 < 5.2:
                answers = [answer, 'This matchup is quite even. Hope you win']

            if float(matchup_number) > 5.2:
                answers = [answer, 'This is a winning matchup, If you lose then you are bad. Go practice']

    return answers

