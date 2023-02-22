from threading import Thread
import Data.screens as sc
import PySimpleGUI as sg
import Data.funct as f
from time import sleep
from PIL import Image
import Data.themes
import Data.config
import json
import time
import sys
import os


class Game:
    run = True
    cancel = False

    def __init__(self):
        self.settings = {
            'theme': 'TamagoDefault',
            'music': 'music1',
            'music_playing': True,
            'music_volume': 100.0,
            'sound_volume': 100.0,
            'portrait_anim': True,
            'scale': 1
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
        window1 = sg.Window('', newGame(self), element_justification='c',
            enable_close_attempted_event=True)

        while True:
            event, values = window1.read(timeout=41.66)

            match event:
                case sg.WINDOW_CLOSE_ATTEMPTED_EVENT | 'Exit':
                    event = sc.popUp(self,'Quit','Are you sure you want to quit?')
                    
                    if event=='OK':
                        sys.exit()

                    if event=='c':
                        continue

                case 'New Pokemon':
                    self.cancel = False

                    while not self.cancel:
                        window1.Hide()
                        sc.new_pokemon_screen(self, player)
                        if player.properties['name']:
                            sc.choose_pokemon(self, player)

                    if player.properties['portrait']:
                        break
                    else:
                        window1.UnHide()
                        continue

                case 'load':
                    self.has_been_called = False
                    window1.Hide()
                    sc.loading_screen(self, player)

                    if self.has_been_called:
                        break
                    else:
                        window1.UnHide()
                        continue

                case 'Settings':
                    self.cancel = False
                    window1.Hide()
                    sc.settings_screen(self)

                    if self.cancel:
                        window1.UnHide()

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

        mainWindow = sg.Window('pokéTamago', mainGame(self, player), icon='data\\img\\logo.ico',
        finalize=True, enable_close_attempted_event=True)

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

                case sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
                    event = sc.popUp(self,'Quit','Are you sure you want to quit?')

                    if event == 'OK':
                        self.run = False
                        break

                    if event == 'c':
                        continue

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
            mainWindow['age'].update(f"{f.time_counter(player.condition['age'])}")
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


def newGame(self):
    match self.settings['theme']:

        case "TamagoDefault":
            titlebar = '#283b5b'

        case "TamagoDark":
            titlebar = '#303134'

        case "TamagoLight":
            titlebar = '#0052e7'

    buttonColumn = [
        [sg.Button('New Pokemon', size=12)],
        [sg.Button('Continue', size=12, key='load')],
        [sg.B('Settings', size=12)],
        [sg.B('Exit', size=12)]
    ]

    elements = [
        [sg.Image('data\\img\\logo.png', subsample=3)],
        [sg.Column(buttonColumn)]
    ]

    frame = [
        [sg.Frame('', elements, relief=sg.RELIEF_FLAT, p=(0,0), element_justification='c')]
    ]

    layout = [
        [sg.Frame('', frame, relief=sg.RELIEF_FLAT, p=(0,0), background_color=titlebar)]
    ]

    return layout


def mainGame(self, player):
    match self.settings['theme']:

        case "TamagoDefault":
            titlebar = '#283b5b'

        case "TamagoDark":
            titlebar = '#303134'

        case "TamagoLight":
            titlebar = '#0052e7'

    condition_layout = [
        [sg.T("Health", font=('', 10, 'bold'))], [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T("Age", font=('', 10, 'bold'))], [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Food", font=('', 10, 'bold'))], [sg.HSeparator(color='#3c4754', p=0)], 
        [sg.T(f"Bored", font=('', 10, 'bold'))], [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Exhausted", font=('', 10, 'bold'))]
    ]

    condition_values = [
        [sg.T(f"{int(player.condition['health'])}", font=('', 10, 'bold'), k='health')],
        [sg.HSeparator(color='#3c4754', p=0)], 
        [sg.T(f"{f.time_counter(player.condition['age'])}", font=('', 10, 'bold'), k='age')],
        [sg.HSeparator(color='#3c4754', p=0)], 
        [sg.ProgressBar(max_value=100, orientation='h', p=0, key='food',)], 
        [sg.HSeparator(color='#3c4754', p=0)], 
        [sg.ProgressBar(max_value=100, orientation='h', p=0, key='bored',)], 
        [sg.HSeparator(color='#3c4754', p=0)], 
        [sg.ProgressBar(max_value=100, orientation='h', p=0, key='exhausted',)]
    ]

    stats_layout = [
        [sg.T(f"Attack", font=('', 10, 'bold'))], [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Defense", font=('', 10, 'bold'))], [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Sp. Attack", font=('', 10, 'bold'))], [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Sp. Defense", font=('', 10, 'bold'))], [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Speed", font=('', 10, 'bold'))]
    ]

    stats_values = [
        [sg.T(f"{int(player.base['Attack'])}", font=('', 10, 'bold'), k='Attack')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{int(player.base['Defense'])}", font=('', 10, 'bold'), k='Defense')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{int(player.base['Sp. Attack'])}", font=('', 10, 'bold'), k='Sp. Attack')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{int(player.base['Sp. Defense'])}", font=('', 10, 'bold'), k='Sp. Defense')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{int(player.base['Speed'])}", font=('', 10, 'bold'), k='Speed')]
    ]

    nameLayout = [
        [sg.T(f"{player.properties['name']}".upper(), font=('', 15, 'bold'))],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Level {player.properties['level']}", font=('', 10), key='level')],
        [sg.ProgressBar(max_value=player.xp_need(), expand_x=True, expand_y=True, orientation='h',
        key='progress_1')],
    ]

    imageLayout = [
        [sg.Graph((170, 100), (0, 100), (170, 0), p=0, key='GRAPH')]
    ]

    if len(player.properties["type"]) < 2:
        TypeImage2 = [
            sg.Image(f'data\\img\\types\\none.png', k='type2', p=0, size=(30, 24), 
            tooltip=' There is no second type of this Pokemon ')
        ]
    else:
        TypeImage2 = [
            sg.Image(f'data\\img\\types\\{player.properties["type"][1]}_Type_Icon.png', k='type2',
            p=0,  size=(30, 24), tooltip=f' {player.properties["type"][1]} ')
        ]

    conditionBar = [
        [sg.Image(f'data\\img\\types\\{player.properties["type"][0]}_Type_Icon.png', k='type1',
        p=0, size=(30, 24), tooltip=f' {player.properties["type"][0]} ')], [sg.HSeparator(color='#3c4754', p=0)],
        TypeImage2, [sg.HSeparator(color='#3c4754', p=0)], [sg.HSeparator(color='#3c4754', p=0)]
    ]

    Column = [
        [sg.Frame('', imageLayout, size=(170, 100), element_justification='c', p=((0, 0), (0, 5))),
         sg.Frame('', conditionBar, size=(30, 100), element_justification='c', p=((0, 0), (0, 5)))],
        [sg.Frame('', nameLayout, size=(200, 90), element_justification='c', p=((0, 0), (5, 5)))],
        [sg.Frame('', condition_layout, size=(100, 142), element_justification='c', p=((0, 0), (5, 5))), 
         sg.Frame('', condition_values, size=(100, 142), element_justification='c', p=((0, 0), (5, 5)))],
        [sg.Frame('', stats_layout, size=(100, 142), element_justification='c', p=((0, 0), (5, 0))),
         sg.Frame('', stats_values, size=(100, 142), element_justification='c', p=((0, 0), (5, 0)))]
    ]

    buttonColumn = [
        [sg.B('Eat', size=8)],
        [sg.B('Play', size=8)],
        [sg.B('Sleep', size=8)],
        [sg.HSeparator(color='#3c4754', p=((0, 0), (10, 10)))],
        [sg.B('Training', size=8)],
        [sg.B('Battle', size=8, disabled=True)],
        [sg.B('Shop', size=8, disabled=True)],
        [sg.HSeparator(color='#3c4754', p=((0, 0), (10, 10)))],
        [sg.B('Main Menu', size=8)],
    ]

    elements = [
        [sg.Column(buttonColumn), sg.Column(Column, element_justification='c')],
    ]

    frame = [
        [sg.Frame('', elements, p=(0,0), element_justification="c", relief=sg.RELIEF_FLAT)]
        ]

    layout = [
        [sg.Frame('', frame, p=(0,0), background_color=titlebar, relief=sg.RELIEF_FLAT)]
    ]

    return layout
