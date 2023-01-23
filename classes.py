import os
import time
import json
import PySimpleGUI as sg
from nickname_generator import generate


class Poke:

    def __init__(self):
        self.stats = {
            "name": "default",
            "portrait": "Data\\img\\poke\\default.gif",
            "type": [],
            "level": 1,
            "xp": 0,
            "MaxHP": 43,
            "Attack": 50,
            "Defense": 53,
            "Sp. Attack": 58,
            "Sp. Defense": 60,
            "Speed": 51
        }

        self.condition = {
            "health": 43,
            "age": 0,
            "bored": 0,
            "food": 100,
            "exhausted": 0
        }

        self.status = {
            "alive": True,
            "revive": False,
            "revive_time": 0,
            "sleeping": False,
            "sleep_time": 0,
            "eating": False,
            "eat_time": 0,
            "training": False,
            "training_time": 0,
            "playing": False,
            "play_time": 0,
            "logoff_time": 0
        }


class Player(Poke):

    def __init__(self):
        super().__init__()


    def open_dex(self):
        pokes = []
        types = []

        with open('Data\pokedex.json', 'r') as read_file:
            data = json.load(read_file)
            for poke in data:
                pokes.append(poke['name'])
                types.append(poke['type'])

        return pokes, types


    def read_save(self):
        directory = 'Data\\save'
        saves = []

        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                saves.append(f.replace('.json', '').replace('Data\\save\\', ''))

        return saves


    def load_saves(self, var):
        self.load_saves.has_been_called = True
        with open(f'Data\save\{var}.json', 'r') as player:
            data = json.load(player)
            self.stats = data['stats']
            self.condition = data['condition']
            self.status = data['status']


    def level_up(self):
        if self.stats['xp'] >= round((4 * ((self.stats['level']+1) ** 3)) / 5):
            self.stats['xp'] = 0
            self.stats['level'] += 1


    def eat(self):
        if self.status['eat_time'] == 0:
            self.status['eating'] = True
            self.status['eat_time'] = 28800
        else:
            sg.popup("You can't feed your pet for now!", title='', keep_on_top=True, auto_close=True,
                     auto_close_duration=3, any_key_closes=True, icon='Data\\img\\warning.ico')


    def training(self):
        if self.status['training_time'] == 0:
            self.status['training_time'] = 86400
            self.condition['food'] -= 5
            self.condition['exhausted'] += 20
            self.stats['xp'] += 5
            if self.condition['bored'] <= 10:
                self.condition['bored'] == 0
            else:
                self.condition['bored'] -= 10


    def play(self):
        if self.status['play_time'] == 0:
            self.condition['food'] -= 2
            self.condition['exhausted'] += 10
            self.stats['xp'] += 1
            if self.condition['bored'] <= 20:
                self.condition['bored'] == 0
            else:
                self.condition['bored'] -= 20


    def sleep(self):
        self.status['sleeping'] = True
        self.status['sleep_time'] = 28800
        self.condition['exhausted'] = 0
        self.condition['bored'] = 0
        self.condition['food'] = 20


    def passing_time(self):
        if self.status["alive"]:
            self.condition['age'] += 1

            self.condition["bored"] += 0.0069
            if self.condition["bored"] > 80:
                self.condition["exhausted"] += 0.01
                if self.condition["bored"] > 100:
                    self.condition["bored"] = 100

            self.condition["food"] -= 0.0034
            if self.condition["food"] < 0:
                self.condition["food"] = 0
                self.condition["health"] -= 0.1

            self.condition["exhausted"] += 0.0023
            if self.condition["exhausted"] >= 100:
                self.condition["health"] -= 0.1
                if self.condition["exhausted"] > 100:
                    self.condition["exhausted"] = 100

            if self.condition['health'] < 0:
                self.condition['health'] = 0
                self.status["alive"] = False

            if self.status['eat_time'] > 0:
                self.status['eat_time'] -= 1
            if self.status['training_time'] > 0:
                self.status['training_time'] -= 1
            if self.status['play_time'] > 0:
                self.status['play_time'] -= 1

        if self.status['revive'] and self.status['revive_time'] > 0:
            self.status['revive_time'] -= 1

        if self.status['sleeping']:
            self.condition['age'] += 1
            self.status['sleep_time'] -= 1


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


class Npc(Poke):

    def __init__(self):
        super().__init__()
        self.stats['name'] = generate()
