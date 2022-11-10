import time
import os
import json
from random import randint

pokes = []
types = []
directory = 'Data\\save'
saves = []


def load_settings(self):
    with open(f'Data\\settings.json', 'r') as settings:
        data = json.load(settings)
        self.settings = data


def save_settings(self):
    if self.settings['theme'] == "TamagoDefault":
        self.settings['background'] = '#516073'
    if self.settings['theme'] == "TamagoDark":
        self.settings['background'] = '#303134'
    if self.settings['theme'] == "TamagoLight":
        self.settings['background'] = '#bfbfb2'

    with open(f"Data\\settings.json", 'w') as settings:
        json.dump(self.settings, settings, indent=4)


def load_saves(self, var):
    load_saves.has_been_called = True
    with open(f'Data\save\{var}.json', 'r') as player:
        data = json.load(player)
        self.stats = data['stats']
        self.condition = data['condition']
        self.status = data['status']


def open_dex():
    with open('Data\pokedex.json', 'r') as read_file:
        data = json.load(read_file)
        for poke in data:
            pokes.append(poke['name'])
            types.append(poke['type'])


def default_player(self):
    with open('Data\\default.json', 'r') as player:
        data = json.load(player)
        self.status = data['status']
        self.condition = data['condition']
        self.stats = data['stats']


def read_save():
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            saves.append(f.replace('.json', '').replace('Data\\save\\', ''))


def offline_time(self):
    then = self.status['logoff_time']
    now = round(time.time())
    elapsed_time = now - then

    if self.status["alive"]:
        self.condition['age'] += elapsed_time
        self.condition["bored"] += (0.0046*elapsed_time)
        self.condition["food"] -= (0.0011*elapsed_time)
        self.condition["exhausted"] += (0.0017*elapsed_time)

        if self.condition["bored"] > 100:
            self.condition["bored"] = 100
        if self.condition["exhausted"] > 100:
            self.condition["exhausted"] = 100
        if self.condition["food"] < 0:
            self.condition["food"] = 0

    if not self.status["alive"] and self.status['revive']:
        if self.status['revive_time'] > elapsed_time:
            self.status['revive_time'] -= elapsed_time
        else:
            self.status['revive_time'] = 0

    if self.status['sleeping']:
        self.condition['age'] += elapsed_time
        if self.status['sleep_time'] > elapsed_time:
            self.status['sleep_time'] -= elapsed_time
        else:
            self.status['sleep_time'] = 0


def time_counter(source):
    days, h_remainder = divmod(source, 86400)
    hrs, remainder = divmod(h_remainder, 3600)
    mins, secs = divmod(remainder, 60)

    age = f"{secs:02}"
    if mins > 0:
        age = f"{mins:02}:{secs:02}"
    if hrs > 0:
        age = f"{hrs:02}:{mins:02}:{secs:02}"
    if days > 0:
        age = f"{days}d {hrs:02}:{mins:02}:{secs:02}"

    return age


def chance(num):
    rng = randint(0, 100)
    miss = False if rng % num == 0 else True
    return miss

