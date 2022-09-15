import json, gui as g, PySimpleGUI as sg

class Poke:
    def __init__(self):
        g.newGame(self)


    def eat(self):
        if self.status['food_cd'] == 0:
            self.status['food_cd'] = 3600
            self.status['food'] = 100
            sg.popup('Eating...', title='', keep_on_top=True, auto_close=True, auto_close_duration=3.5, icon='Data\img\dish.ico')
        else:
            sg.popup('You can not do that right now!', title='Oops!', keep_on_top=True, auto_close=True, auto_close_duration=3, icon='Data\img\dish.ico')


    def training(self):
        if self.status['training_cd'] == 0:
            self.status['training_cd'] = 7200
            self.status['food'] -= 5
            self.status['exhausted'] += 20
            self.stats['xp'] += 5
            if self.status['bored'] <= 10:
                self.status['bored'] == 0
            else:
                self.status['bored'] -= 10
            sg.popup('Working out...', title='', keep_on_top=True, auto_close=True, auto_close_duration=6, icon='Data\img\dish.ico')
        else:
            sg.popup('You can not do that right now!', title='Oops!', keep_on_top=True, auto_close=True, auto_close_duration=3, icon='Data\img\dish.ico')


    def play(self):
        if self.status['play_cd'] == 0:
            self.status['food'] -= 2
            self.status['exhausted'] += 10
            self.stats['xp'] += 1
            if self.status['bored'] <= 20:
                self.status['bored'] == 0
            else:
                self.status['bored'] -= 20
            sg.popup('Playing...', title='', keep_on_top=True, auto_close=True, auto_close_duration=4, icon='Data\img\dish.ico')
        else:
            sg.popup('You can not do that right now!', title='Oops!', keep_on_top=True, auto_close=True, auto_close_duration=3, icon='Data\img\dish.ico')

    def sleep(self):
        self.status['exhausted'] = 0
        self.status['food'] = 20
        sg.popup('Sleeping...', title='', keep_on_top=True, auto_close=True, auto_close_duration=10, icon='Data\img\dish.ico')
        

    def passing_time(self):
        self.status['age'] += 1
        self.status["bored"] += 0.0046
        self.status["food"] -= 0.0011
        self.status["exhausted"] += 0.0017

        if self.status["bored"] > 80:
            self.status["exhausted"] += 0.01
            if self.status["bored"] > 100:
                self.status["bored"] = 100

        if self.status["food"] < 0:
            self.status["food"] = 0
            self.status["health"] -= 0.1

        if self.status["exhausted"] >= 100:
            self.status["health"] -= 0.1
            if self.status["exhausted"] > 100:
                self.status["exhausted"] = 100

        if self.status['health'] <= 0:
            self.status["alive"] = False

        if self.status['eat_cd'] > 0:
            self.status['eat_cd'] -= 1
        else:
           self.status['eat_cd'] = 0

        if self.status['training_cd'] > 0:
            self.status['training_cd'] -= 1
        else:
           self.status['training_cd'] = 0

        if self.status['play_cd'] > 0:
            self.status['play_cd'] -= 1
        else:
           self.status['play_cd'] = 0


    def autosave(self):
        save = {}
        save['stats'] = self.stats
        save['status'] = self.status
        with open(f"Data\save\{self.stats['name']}.json", 'w') as outfile:
            json.dump(save, outfile)


    def run(self):
        g.mainGame(self)