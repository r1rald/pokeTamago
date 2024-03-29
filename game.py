from threading import Thread
import PySimpleGUI as sg
import ui_screens as sc
import ui_layout as ui
from time import sleep
from PIL import Image
from re import sub
import Data.themes
import funct as f
import json
import time
import sys
import os


class Game:
    run = True
    cancel = False

    def __init__(self):
        self.settings = {
            "theme": "TamagoDefault",
            "background": "#516073",
            "music": "music1",
            "music_playing": True,
            "music_volume": 100.0,
            "sound_volume": 100.0,
            "portrait_anim": True
        }
        
        path = os.path.expanduser('~\\Documents\\pokeTamago\\cfg')

        if os.path.exists(os.path.expanduser('~\\Documents\\pokeTamago\\cfg')):
            with open(f'{path}\\settings.json', 'r') as settings:
                data = json.load(settings)
                self.settings = data
        else:
            os.makedirs(path)
            self.save_settings()

        sg.theme(self.settings['theme'])
        f.randomYieldGroup()

    def newGame(self, player):
        window1 = sg.Window('', ui.newGame(), icon='data\\img\\logo.ico', element_justification='c',
        grab_anywhere=True)

        while True:
            event, values = window1.read(timeout=100)

            match event:
                case sg.WIN_CLOSED | 'Exit':
                    sys.exit()

                case 'New Pokemon':
                    self.cancel = False

                    while not self.cancel:
                        sc.new_pokemon_screen(self, player)
                        if player.properties['name']:
                            sc.choose_pokemon(self, player)

                    if player.properties['portrait']:
                        break
                    else:
                        continue

                case 'load':
                    self.has_been_called = False
                    sc.loading_screen(self, player)
                    if self.has_been_called:
                        break
                    else:
                        continue

                case 'Settings':
                    sc.settings_screen(self)

            if not self.read_save():
                window1['load'].update(disabled=True)
            else:
                window1['load'].update(disabled=False)

        window1.close()

    def mainGame(self, player):
        global index, frames, size

        def portrait_thread():
            global index, frames
            while True:
                sleep(0.03)
                index = (index + 1) % frames
                if not self.run:
                    break

        im = Image.open(player.properties['portrait'])

        width, height = im.size
        frames = im.n_frames

        graph_width, graph_height = size = (170, 100)

        mainWindow = sg.Window('pokéTamago', ui.mainGame(self, player), icon='data\\img\\logo.ico', 
        finalize=True)

        mainWindow['GRAPH'].draw_image(f'{f.portrait_background(player)}', location=(0, 0))

        index = 1

        im.seek(index)

        location = (graph_width//2-width//2, graph_height//2-height//2)

        item = mainWindow['GRAPH'].draw_image(data=f.image_to_data(im),location=location)

        thread = Thread(target=portrait_thread, daemon=True)
        if self.settings['portrait_anim']:
            thread.start()

        while True:
            event, value = mainWindow.read(timeout=41.66)

            match event:
                case sg.TIMEOUT_KEY:
                    im.seek(index)
                    item_new = mainWindow['GRAPH'].draw_image(data=f.image_to_data(im), location=location)
                    mainWindow['GRAPH'].delete_figure(item)
                    item = item_new
                    mainWindow.refresh()

                case sg.WIN_CLOSED:
                    self.run = False
                    break

                case 'Eat':
                    sc.eat_screen(self, player)

                case 'Battle':
                    pass

                case 'Training':
                    sc.train_screen(self, player)

                case 'Play':
                    sc.play_screen(self, player)

                case 'Sleep':
                    sc.sleep_screen(self, player)
                    
                case 'Main Menu':
                    self.run = False
                    os.execl(sys.executable, sys.executable, *sys.argv)

            if not player.status['alive']:
                sc.death_screen(self, player)
            if player.status['sleeping']:
                sc.sleep_screen(self, player)

            if 40 < player.condition["food"]:
                fdClr = (None)
            elif 20 < player.condition["food"] < 40:
                fdClr = ('orange', 'white')
            else:
                fdClr = ('red', 'white')

            if player.condition["bored"] < 60:
                brdClr = (None)
            elif 60 < player.condition["bored"] < 80:
                brdClr = ('orange', 'white')
            else:
                brdClr = ('red', 'white')

            if player.condition["exhausted"] < 60:
                xhstdClr = (None)
            elif 60 < player.condition["exhausted"] < 80:
                xhstdClr = ('orange', 'white')
            else:
                xhstdClr = ('red', 'white')

            mainWindow['progress_1'].update(int(player.properties['xp']), max=player.xp_need())
            mainWindow['level'].update(f"Level {player.properties['level']}")
            mainWindow['health'].update(int(player.condition['health']))
            mainWindow['age'].update(f.time_counter(player.condition['age']))
            mainWindow['food'].update(int(player.condition['food']), bar_color=fdClr)
            mainWindow['bored'].update(int(player.condition['bored']), bar_color=brdClr)
            mainWindow['exhausted'].update(int(player.condition['exhausted']), bar_color=xhstdClr)
            mainWindow['Attack'].update(int(player.base['Attack']))
            mainWindow['Defense'].update(int(player.base['Defense']))
            mainWindow['Sp. Attack'].update(int(player.base['Sp. Attack']))
            mainWindow['Sp. Defense'].update(int(player.base['Sp. Defense']))
            mainWindow['Speed'].update(int(player.base['Speed']))

        mainWindow.close()

    def autosave(self, player):
        save = {}

        save['properties'] = player.properties
        save['base'] = player.base
        save['condition'] = player.condition
        save['status'] = player.status
        player.status['logoff_time'] = round(time.time())

        path = os.path.expanduser('~\\Documents\\pokeTamago\\save')
        
        with open(f"{path}\\{player.properties['name']}.json", 'w') as outfile:
            json.dump(save, outfile, indent=4)

    def save_settings(self):
        path = os.path.expanduser('~\\Documents\\pokeTamago\\cfg')

        if self.settings['theme'] == "TamagoDefault":
            self.settings['background'] = '#516073'
        if self.settings['theme'] == "TamagoDark":
            self.settings['background'] = '#303134'
        if self.settings['theme'] == "TamagoLight":
            self.settings['background'] = '#bfbfb2'

        with open(f"{path}\\settings.json", 'w') as settings: 
            json.dump(self.settings, settings, indent=4)

    def open_dex(self):
        pokes = ([], [], [], [])

        with open('data\\pokedex.json', 'r') as read_file:
            data = json.load(read_file)
            for poke in data:
                pokes[0].append(poke['name'])
                pokes[1].append(poke['type'])
                pokes[2].append(poke['xp_group'])
                pokes[3].append(poke['yield'])

        return pokes

    def read_save(self):
        saves = []
        
        if os.path.exists(os.path.expanduser('~\\Documents\\pokeTamago\\save')):
            for save in os.listdir(os.path.expanduser('~\\Documents\\pokeTamago\\save')):
                saves.append(save.replace('.json', ''))
        else:
            os.makedirs(os.path.expanduser('~\\Documents\\pokeTamago\\save'))

        return saves


    def load_saves(self, player, var):
        self.has_been_called = True

        path = os.path.expanduser('~\\Documents\\pokeTamago\\save')

        with open(os.path.expanduser(f'{path}\\{var}.json'), 'r') as load:
            data = json.load(load)

            player.properties = data['properties']
            player.base = data['base']
            player.condition = data['condition']
            player.status = data['status']
