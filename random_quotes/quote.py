import random
import json
from pathlib import Path

cwd = Path.cwd()

def get_random_quote():
    with open(str(cwd)+'/random_quotes/gamer_quotes.json','r',encoding="utf-8") as quotes:
        data = json.load(quotes)
    quote = random.choice(data['quotes'])
    return str(quote)