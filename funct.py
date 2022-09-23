import time, os, json

def load_saves(self, var):
    with open(f'Data\save\{var}.json', 'r') as player:
        data = json.load(player)
        self.stats = data['stats']
        self.condition = data['condition']
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
    with open('Data\\Player.json', 'r') as player:
        data = json.load(player)
        self.status = data['status']
        self.condition = data['condition']
        self.stats = data['stats']


directory = 'Data\\save'
saves = []
def read_save():
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            saves.append(f.replace('.json', '').replace('Data\\save\\', ''))


def offline_time(self):
    then = self.status['time']
    now = round(time.time())
    elapsed_time = now - then
    
    if self.status["alive"]:
        self.condition['age'] += elapsed_time
        self.condition["bored"] += (0.0046*elapsed_time)
        self.condition["food"] -= (0.0011*elapsed_time)
        self.condition["exhausted"] += (0.0017*elapsed_time)

        if self.condition["bored"] > 100:
            self.condition["bored"] = 100

        if self.condition["food"] < 0:
            self.condition["food"] = 0

        if self.condition["exhausted"] >= 120:
            self.condition["exhausted"] = 120
    else:
        if self.status['revive']:
            if self.status['revive_time'] > 0 and self.status['revive_time'] < elapsed_time:
                self.status['revive_time'] -= elapsed_time
            else:
                self.status['revive_time'] = 0

def process_time(source):
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