import json, gui as g, PySimpleGUI as sg

class Poke:
    run = True

    def __init__(self):
        g.newGame(self)


    def eat(self):
        if self.status['food_cd'] == 0:
            self.status['food_cd'] = 3600
            self.condition['food'] = 100
            sg.popup('Eating...', title='', keep_on_top=True, auto_close=True, auto_close_duration=3.5, icon='Data\img\dish.ico')
        else:
            sg.popup('You can not do that right now!', title='Oops!', keep_on_top=True, auto_close=True, auto_close_duration=3, icon='Data\img\dish.ico')


    def training(self):
        if self.status['training_cd'] == 0:
            self.status['training_cd'] = 7200
            self.status['food'] -= 5
            self.condition['exhausted'] += 20
            self.stats['xp'] += 5
            if self.condition['bored'] <= 10:
                self.condition['bored'] == 0
            else:
                self.condition['bored'] -= 10
            sg.popup('Working out...', title='', keep_on_top=True, auto_close=True, auto_close_duration=6, icon='Data\img\dish.ico')
        else:
            sg.popup('You can not do that right now!', title='Oops!', keep_on_top=True, auto_close=True, auto_close_duration=3, icon='Data\img\dish.ico')


    def play(self):
        if self.status['play_cd'] == 0:
            self.condition['food'] -= 2
            self.condition['exhausted'] += 10
            self.stats['xp'] += 1
            if self.condition['bored'] <= 20:
                self.condition['bored'] == 0
            else:
                self.condition['bored'] -= 20
            sg.popup('Playing...', title='', keep_on_top=True, auto_close=True, auto_close_duration=4, icon='Data\img\dish.ico')
        else:
            sg.popup('You can not do that right now!', title='Oops!', keep_on_top=True, auto_close=True, auto_close_duration=3, icon='Data\img\dish.ico')

    def sleep(self):
        self.condition['exhausted'] = 0
        self.condition['food'] = 20
        sg.popup('Sleeping...', title='', keep_on_top=True, auto_close=True, auto_close_duration=10, icon='Data\img\dish.ico')
        

    def passing_time(self):
        self.condition['age'] += 1
        self.condition["bored"] += 0.0069
        self.condition["food"] -= 0.0034
        self.condition["exhausted"] += 0.0023

        if self.condition["bored"] > 80:
            self.condition["exhausted"] += 0.01
            if self.condition["bored"] > 100:
                self.condition["bored"] = 100

        if self.condition["food"] < 0:
            self.condition["food"] = 0
            self.condition["health"] -= 0.1

        if self.condition["exhausted"] >= 100:
            self.condition["health"] -= 0.1
            if self.condition["exhausted"] > 100:
                self.condition["exhausted"] = 100

        if self.condition['health'] <= 0:
            self.condition["alive"] = False

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
        save['condition'] = self.condition
        save['status'] = self.status
        with open(f"Data\save\{self.stats['name']}.json", 'w') as outfile:
            json.dump(save, outfile)


    def run(self):
        g.mainGame(self)