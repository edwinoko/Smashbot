import requests
from bs4 import BeautifulSoup
from datetime import datetime
from os import link, mkdir,path
from pathlib import Path
import json

site = 'https://www.eventhubs.com'

def get_data():

    link = site
    data = requests.get(link+'/tiers/ssbu')
    page = data.content

    character_links = clean_data(page)

    return character_links

def clean_data(page):

    soup = BeautifulSoup(page, 'html.parser')
    edited_soup = soup.find('table').find_all('a')

    links = []

    for link in edited_soup:
        if link.has_attr('href'):
            if not 'vote' in link['href']:
                links.append(link['href'])

    get_matchups(links)

    #return links

def get_matchups(links):

    for link in links:
        #print(link.split('/')[-1])
        pagina = requests.get(site+link)
        soup = BeautifulSoup(pagina.content, 'html.parser')
        edited_soup = soup.find(class_='two-thirds column').find_all(class_='tierstable')#[0:-1]
        linked_data = get_link_data(edited_soup, link.split('/')[-1])
        #print(linked_data)
        feedback = write_matchup_to_file(link.split('/')[-1],linked_data)

        #print(len(edited_soup))
    return feedback
     

def get_link_data(soup, character_name):
    matchup_dict = {}
    for section in soup:
        #print(section)
        #stew = BeautifulSoup(section, 'html.parser')
        tasty_stew = section.find_all(class_=('even')) + section.find_all(class_=('odd'))
        #print(len(tasty_stew))
        #print(tasty_stew[2])
        for entry in tasty_stew:
            name = ''
            value = ''
            for line in entry.find_all(class_='tierstdnorm')[1:]:

                if not '-' in line.getText():
                    try:
                        numeric_value = float(line.getText())
                        if numeric_value < 10 and numeric_value > 1:
                            value = numeric_value
                            break
                    except:    
                        #print(line.getText()+' this is not a number silly goose')
                        name = line.getText().lower().replace(' ','-')
            #matchup_dict = {}
            matchup_dict[name] = value
    
    #print({character_name : matchup_dict})
    return {character_name : matchup_dict}
    
def write_matchup_to_file(title,character_data):
    cwd = str(Path.cwd())

        # check whether the character file exists
    if not path.exists(cwd+'/matchup_data/'+title+'.json'): 
        #creating a file    
        with open(cwd+'/matchup_data/'+title+'.json','w+') as char_file:
            char_file.write(json.dumps(character_data))

    return 'we gucci my homie'
