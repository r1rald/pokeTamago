import json, time, main_ui as g, PySimpleGUI as sg

class Poke:
    run = True

    def __init__(self):
        g.newGame(self)


    def eat(self):
        if self.status['eat_time'] == 0:
            self.status['eating'] = True
            #self.status['eat_time'] = 28800
        else:
            sg.popup("You can't feed your pet for now!",title='',keep_on_top=True, auto_close=True, auto_close_duration=3,any_key_closes=True,icon='Data\\img\\warning.ico')

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



    def autosave(self):
        save = {}
        save['stats'] = self.stats
        save['condition'] = self.condition
        save['status'] = self.status
        self.status['logoff_time'] = round(time.time())
        with open(f"Data\\save\\{self.stats['name']}.json", 'w') as outfile:
            json.dump(save, outfile,indent=4)


    def run(self):
        g.mainGame(self)