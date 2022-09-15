import time, os, json

def load_saves(self, var):
    with open(f'Data\save\{var}.json', 'r') as player:
        data = json.load(player)
        self.stats = data['stats']
        self.status = data['status']


pokes = []
types = []
def open_dex():
    with open('Data\pokedex.json', 'r') as read_file:
        data = json.load(read_file)
        for poke in data:
            pokes.append(poke['name'])
            types.append(poke['type'])


def default_player(self):
    with open('Data\Player.json', 'r') as player:
        data = json.load(player)
        self.status = data['status']
        self.stats = data['stats']


directory = 'Data\save'
saves = []
def read_save():
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            saves.append(f.replace('.json', '').replace('Data\save\\', ''))


def offline_time(self):
    then = self.status['time']
    now = round(time.time())
    elapsed_time = now - then

    self.status['age'] += (1*elapsed_time)
    self.status["bored"] += (0.0001*elapsed_time)
    self.status["food"] -= (0.0001*elapsed_time)
    self.status["exhausted"] += (0.0001*elapsed_time)

    if self.status["bored"] > 100:
        self.status["bored"] = 100

    if self.status["food"] < 0:
        self.status["food"] = 0

    if self.status["exhausted"] >= 120:
        self.status["exhausted"] = 120
