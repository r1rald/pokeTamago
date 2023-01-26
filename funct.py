from io import BytesIO
import datetime
import random
import json


def randomYieldGroup():
    xp_group = ['Medium Slow', 'Medium Fast', 'Fast', 'Slow']

    with open("Data\\pokedex.json", "r") as read_file:
        data = json.load(read_file)

        for i in data:
            a = {"xp_group": random.choice(xp_group), "yield": random.randint(36,340)}
            i.update(a)

    with open("Data\\pokedex.json", "w") as write_file:
        json.dump(data, write_file)


def image_to_data(im):
    with BytesIO() as output:
        im.save(output, format="PNG")
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
        bg = f'Data\\img\\poke\\BG\\grassland-feild-{partOfAday()}.png'
    elif player.properties['type'][0] in forest:
         bg = f'Data\\img\\poke\\BG\\forest-grassy-{partOfAday()}.png'
    elif player.properties['type'][0] in mountaintop:
         bg = f'Data\\img\\poke\\BG\\mountaintop-high-{partOfAday()}.png'
    elif player.properties['type'][0] == 'Water':
         bg = f'Data\\img\\poke\\BG\\ocean-water-{partOfAday()}.png'
    elif player.properties['type'][0] == 'Ice':
         bg = f'Data\\img\\poke\\BG\\snowy-{partOfAday()}.png'
    else:
        if partOfAday() == 'day' or partOfAday() == 'afternoon':
             bg = 'Data\\img\\poke\\BG\\cave-day.png'
        else:
             bg = 'Data\\img\\poke\\BG\\cave-night.png'   

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
