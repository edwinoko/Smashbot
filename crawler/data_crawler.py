import requests
from bs4 import BeautifulSoup
from datetime import datetime
from os import mkdir,path
from pathlib import Path
import json

'''
These classes and functions are responsible for getting the frame data and images from ultimateframedata.com and writing them away locally.
every character entry has a timestamp inorder to check when the data was querried. This information is stored in a singelton dictionary in 
memory and also in a json file in the raw_data folder. If this is the first time starting the bot then run get_data() and let it get all 
the information it needs. This might take awhile tho so go play a game in the meantime.
'''

site='https://ultimateframedata.com/'


class CharacterList:
   __instance = {}

   @staticmethod 
   def getInstance():
      """ Static access method. """
      if CharacterList.__instance == dict:
         CharacterList()
      return CharacterList.__instance
        
   def __init__(self):
      """ Virtually private constructor. """
      if CharacterList.__instance != dict:
         raise Exception("This class is a singleton!")
      else:
         CharacterList.__instance = self

# Where are we getting the data from. Als check the last time all the data was gotten and if it is more than 3 months then redownload everything

def get_data():
    link = site
    # check if the date file exist if not create it.
    cwd = str(Path.cwd())
    if  not path.exists(cwd+'/rawdata/datefile'):

        with open(cwd+'/rawdata/datefile','w+') as char_file:
            char_file.write(str(datetime.now()))
        
        data = requests.get(link)
        page = data.content
    
        cleaned_data = clean_data(page)

        return cleaned_data
''' 
    # check if the date in the date file is more than 3 months old
    else:
        f = open(cwd+'/rawdata/datefile','r')
        lines = f.readlines()

        for line in lines:
            try:
                date = datetime(line)

                days_gone = datetime.now() - date

                if days_gone > 90:
                    data = requests.get(link)
                    page = data.content
    
                    cleaned_data = clean_data(page)

                    with open(cwd+'/rawdata/datefile','w') as char_file:
                        char_file.write(str(datetime.now()))
        
                return cleaned_data

            except:
                print('someting went wrong with the dates')
        
'''


    # if it is, then redownload everything. I have already added dates to the individual files for optimization later down the road
    

# cleaning the data
def clean_data(data):

    stew = BeautifulSoup(data, 'html.parser')
    raw_character_list = stew.find(id='charList').find_all('a')

# on the first page there is a list that links to all the individual characters. This is looped over with the use of bs4. The first one
# talks about general stats which is being skipped in the loop. The links are passed to the next function inorder to get the data from
# each link. Uncomment the break if you want to load all the characters.
    for character in raw_character_list[1:]:
        x=create_local_data_structure(character.get('title'), character.get('href'))
        #break

    return x


# This function gets the link and sorts them neatly into a dict.
def get_character_data(link):

    webpage = requests.get(site+link)
    content = webpage.content
    soup = BeautifulSoup(content, 'html.parser')
    
    #list of all moves for one character.
    all_moves = soup.find(id="contentcontainer").find_all(class_="movecontainer")

    nice_moves = {}
    nice_entry = {}

    for move in all_moves:
        move_data = move.find_all('div')
        movename = 'move'
        for entry in move_data:
            #movename = 'move'
            # grabbing link for the gif from the string
            try:

                # getting the picture of the hitbox
                gif=entry.find('a')
                nice_entry[entry['class'][0]] = gif['data-featherlight']

            except:
                try:

                    # noting all other entries like landing lag and all that good stuff. The movename is used as the key for all the
                    # frame data
                    if str(entry['class'][0]) == 'movename':
                        movename = entry.getText().strip().lower().replace(' ','_').replace('.','')
                        nice_entry[entry['class'][0]] = entry.getText().strip()

                    else:

                        nice_entry[entry['class'][0]] = entry.getText().strip()

                except KeyError:

                    # need to fix this but not a pro right now
                    print('sss')

        nice_moves[movename] = {}
        nice_moves[movename].update(nice_entry)
        #print(movename)
        #print(nice_entry)
        #break

    print(nice_moves)

    return nice_moves


#This function links the character website information with the moves found in the link and returns a dict with the combined information.
def create_local_data_structure(title, url):
    title = title.strip().lower().replace(' ','_')

    moves = get_character_data(url)

    x = CharacterList.getInstance()
    x[title] = {'url': url, 'date': str(datetime.now()) ,'moves': moves}

    character_data = {'url': url, 'date': str(datetime.now()) ,'moves': moves}


    # creating a file for each character

    cwd = str(Path.cwd())

    # check whether the character file exists
    if not path.exists(cwd+'/smash_character_data/'+title+'.json'):
        
    #creating a file    
        with open(cwd+'/smash_character_data/'+title+'.json','w+') as char_file:
            char_file.write(json.dumps(character_data))
       
    return x

#x = get_data()
#print('It has been done')