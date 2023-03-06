from io import BytesIO
from PIL import Image
import datetime
import random
import json


def poke_randomizer():
    xp_group = [
        'Medium Slow', 'Medium Fast', 'Fast', 'Slow'
        ]
    nature = ['Hardy', 'Lonely', 'Brave', 'Adamant', 'Naughty', 'Bold', 'Docile', 'Relaxed', 
        'Impish', 'Lax', 'Timid', 'Hasty', 'Serious', 'Jolly', 'Naive', 'Modest', 'Mild',
        'Quiet', 'Bashful', 'Rash', 'Calm', 'Gentle', 'Sassy', 'Careful', 'Quirky']

    with open("src\\cfg\\pokedex.json", "r") as read_file:
        data = json.load(read_file)

        for i in data:
            a = {
                "nature": random.choice(nature),
                "xp_group": random.choice(xp_group),
                "yield": random.randint(36,340)
            }

            i.update(a)

        for j in data:
            b = {
                'HP_IV': random.randint(0,31),
                'Attack_IV': random.randint(0,31),
                'Defense_IV': random.randint(0,31),
                'Sp. Attack_IV': random.randint(0,31),
                'Sp. Defense_IV': random.randint(0,31),
                'Speed_IV': random.randint(0,31)
            }

            j['base'].update(b)

        for x in data:
            c = {
                'HP_EV': 0,
                'Attack_EV': 0,
                'Defense_EV': 0,
                'Sp. Attack_EV': 0,
                'Sp. Defense_EV': 0,
                'Speed_EV': 0
            }

            x['base'].update(c)

            for y in range(3):
                ev = ['HP_EV', 'Attack_EV', 'Defense_EV', 'Sp. Attack_EV', 'Sp. Defense_EV','Speed_EV']
                random_key = random.choice(ev)
                x['base'][random_key] = 1


    with open("src\\cfg\\pokedex.json", "w") as write_file:
        json.dump(data, write_file)


def image2data(im=None,resize=False,path='',size=1):
    if resize:
        image = Image.open(f'src\\assets\\img\\{path}.png')
        width, height = image.size
        im = image.resize((int(width*size), int(height*size)))

    with BytesIO() as output:
        im.save(output, format='PNG')
        data = output.getvalue()

    return data


def portrait_background(player):
    grassland = ['Normal', 'Fire', 'Electric', 'Psychic', 'Fairy']
    forest = ['Poison', 'Bug', 'Grass']
    mountaintop = ['Fighting', 'Flying', 'Ground', 'Rock', 'Dragon']

    def partOfAday():
        current_time = datetime.datetime.now().hour
        return 'day' if 5 <= current_time <= 14 else 'afternoon' if 15 <= current_time <= 20 else 'night'

    if player.properties['type'][0] in grassland :
        bg = f'src\\assets\\img\\bg\\grassland-feild-{partOfAday()}.png'
    elif player.properties['type'][0] in forest:
         bg = f'src\\assets\\img\\bg\\forest-grassy-{partOfAday()}.png'
    elif player.properties['type'][0] in mountaintop:
         bg = f'src\\assets\\img\\bg\\mountaintop-high-{partOfAday()}.png'
    elif player.properties['type'][0] == 'Water':
         bg = f'src\\assets\\img\\bg\\ocean-water-{partOfAday()}.png'
    elif player.properties['type'][0] == 'Ice':
         bg = f'src\\assets\\img\\bg\\snowy-{partOfAday()}.png'
    else:
        if partOfAday() == 'day' or partOfAday() == 'afternoon':
             bg = 'src\\assets\\img\\bg\\cave-day.png'
        else:
             bg = 'src\\assets\\img\\bg\\cave-night.png'   

    return bg


def time_counter(source):
    days, h_remainder = divmod(source, 86400)
    hrs, remainder = divmod(h_remainder, 3600)
    mins, secs = divmod(remainder, 60)

    age = f"{mins:02}:{secs:02}"
    
    if hrs > 0:
        age = f"{hrs:02}:{mins:02}:{secs:02}"
    if days > 0:
        age = f"{days}d {hrs:02}:{mins:02}:{secs:02}"

    return age


def hp_formula(base,iv,ev,level):
    return ((((base+iv)*2+(ev/4))*level)/100)+level+10


def stat_formula(base,iv,ev,level):
    return ((((base+iv)*2+(ev/4))*level)/100)+5
