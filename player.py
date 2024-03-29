from nickname_generator import generate
from random import choice
import PySimpleGUI as sg
import time
import json


class Poke:

    def __init__(self):
        self.properties = {
            "name": None,
            "portrait": None,
            "type": [],
            "level": 1,
            "xp": 0,
            "xp_group": None,
            "yield": None
        }
        
        self.base = {
            "Attack": 50,
            "Defense": 53,
            "Sp. Attack": 58,
            "Sp. Defense": 60,
            "Speed": 51
        }

        self.condition = {
            "MaxHP" : 43,
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


    def xp_need(self):
        level = self.properties['level']

        match self.properties["xp_group"]:
            case "Fast":
                need = int((4 * (level ** 3)) / 5)

            case "Medium Fast":
                need = int(level ** 3)

            case "Medium Slow":
                need = int(((6 / 5) * (level ** 3)) - (15 * (level ** 2)) + (100 * level)-140)
                
            case "Slow":
                need = int((5 * (level ** 3)) / 4)

        return need



    def level_up(self):   
        level = self.properties['level']
        xp = self.properties['xp']

        if xp >= self.xp_need() and level < 100:
            self.properties['xp'] = 0
            self.properties['level'] += 1

            self.base["Attack"] += round(self.base["Attack"]/50, 2)
            self.base["Defense"] += round(self.base["Defense"]/50, 2)
            self.base["Sp. Attack"] += round(self.base["Sp. Attack"]/50, 2)
            self.base["Sp. Defense"] += round(self.base["Sp. Defense"]/50, 2)
            self.base["Speed"] += round(self.base["Speed"]/50, 2)

            #"MaxHP" : 43,
            #self.condition['health'] = self.condition['MaxHP']


    def eat(self):
        self.status['eating'] = True
        if self.status['eat_time'] == 0:
            self.status['eat_time'] = 28800
            self.condition['food'] += 50
            if self.condition['food'] > 100:
                self.condition['food'] = 100


    def training(self):
        self.status['training'] = True
        if self.status['training_time'] == 0:
            self.status['training_time'] = 28800
            self.condition['food'] -= 25
            self.condition['exhausted'] += 25
            self.properties['xp'] += 5
            self.condition['bored'] -= 10 if self.condition['bored'] > 0 else 0
            if self.condition['exhausted'] > 100:
                self.condition['exhausted'] = 100
            if self.condition['food'] < 0:
                self.condition['food'] = 0

        self.level_up()


    def play(self):
        self.status['playing'] = True
        if self.condition['exhausted'] < 90:
            self.condition['food'] -= 2 if self.condition['food'] > 0 else 0
            self.condition['exhausted'] += 10 if self.condition['exhausted'] < 100 else 0
            self.properties['xp'] += 1
            self.condition['bored'] -= 20 if self.condition['bored'] > 0 else 0

        self.level_up()


    def sleep(self):
        self.status['sleeping'] = True
        if self.status['sleep_time'] == 0:
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
            if self.status['sleep_time'] > elapsed_time:
                self.status['sleep_time'] -= elapsed_time
            else:
                self.status['sleep_time'] = 0

        if self.status['eating']:
            if self.status['eat_time'] > elapsed_time:
                self.status['eat_time'] -= elapsed_time
            else:
                self.status['eat_time'] = 0

        if self.status['training']:
            if self.status['training_time'] > elapsed_time:
                self.status['training_time'] -= elapsed_time
            else:
                self.status['training_time'] = 0

        if self.status['playing']:
            if self.status['play_time'] > elapsed_time:
                self.status['play_time'] -= elapsed_time
            else:
                self.status['play_time'] = 0


class Npc(Poke):

    def __init__(self):
        super().__init__()
        self.properties["name"] = generate()
        self.properties["level"] = Player().properties["level"]
        self.xp = int(((self.properties["yield"]*self.properties["level"])/7))
    
    
    def open_dex():
        player = sum(Player().base.values())
        pokes = []

        with open('data\pokedex.json', 'r') as read_file:
            data = json.load(read_file)
            for poke in data:
                if (player-10) < sum(poke['base'].values()) < (player+10):
                    pokes.append(poke["name"])

        return choice(pokes)
