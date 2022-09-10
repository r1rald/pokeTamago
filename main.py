import PySimpleGUI as sg, gui as g
import json, time, threading, sched


class Player:
    food_cd = 0


    def __init__(self):
        g.newGame(self)


    def eat(self):
        if self.food_cd == 0:
            self.food_cd = 3600
            self.status['food'] = 100
            sg.popup('Eating...', title='', keep_on_top=True, auto_close=True, auto_close_duration=3.5, icon='Data\img\dish.ico')
        else:
            sg.popup('You can not do that right now!', title='Oops!', keep_on_top=True, auto_close=True, auto_close_duration=3, icon='Data\img\dish.ico')


    def training(self):
        self.status['food'] -= 5
        self.status['exhausted'] += 20
        self.stats['xp'] += 5
        if self.status['bored'] <= 10:
            self.status['bored'] == 0
        else:
            self.status['bored'] -= 10
        sg.popup('Working out...', title='', keep_on_top=True, auto_close=True, auto_close_duration=6, icon='Data\img\dish.ico')
        return ('Working out...', 6)


    def play(self):
        self.status['food'] -= 2
        self.status['exhausted'] += 10
        self.stats['xp'] += 1
        if self.status['bored'] <= 20:
            self.status['bored'] == 0
        else:
            self.status['bored'] -= 20
        sg.popup('Playing...', title='', keep_on_top=True, auto_close=True, auto_close_duration=4, icon='Data\img\dish.ico')
        return ('Playing a game...', 4)


    def sleep(self):
        self.status['exhausted'] = 0
        self.status['food'] = 20
        sg.popup('Sleeping...', title='', keep_on_top=True, auto_close=True, auto_close_duration=10, icon='Data\img\dish.ico')
        return ('Sleeping...', 10)
        

    def passing_time(self):
        self.status['age'] += 1
        self.status["bored"] += 0.055
        self.status["food"] -= 0.027
        self.status["exhausted"] += 0.033

        if self.status["bored"] > 80:
            self.status["exhausted"] += 0.1
            if self.status["bored"] > 100:
                self.status["bored"] = 100

        if self.status["food"] < 0:
            self.status["food"] = 0
            self.status["health"] -= 0.1

        if self.status["exhausted"] >= 100:
            self.status["health"] -= 0.1
            if self.status["exhausted"] >= 120:
                self.status["exhausted"] = 120

        if self.status['health'] <= 0:
            self.status["alive"] = False

        if self.food_cd > 0:
            self.food_cd -= 1
        else:
           self.food_cd = 0


    def autosave(self):
        save = {}
        save['stats'] = self.stats
        save['status'] = self.status
        with open(f"Data\save\{self.stats['name']}.json", 'w') as outfile:
            json.dump(save, outfile)


    def run(self):
        g.mainGame(self)


def main():
    poke = Player()

    s = sched.scheduler(time.time, time.sleep)

    def run(sc):
        poke.autosave()
        poke.passing_time()
        if poke.status["alive"]:
            s.enter(1, 1, run, (sc,))

    s.enter(1, 1, run, (s,))
    t = threading.Thread(target=s.run)
    t.start()

    while poke.status['alive']:
        poke.run()

if __name__ == "__main__":
    main()