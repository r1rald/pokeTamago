from nickname_generator import generate
from regex import search, sub
from threading import Thread
import src.hooks.funct as f
import src.components as c
import PySimpleGUI as sg
from time import sleep
from PIL import Image
import src.cfg.themes
import src.cfg.config
import json
import time
import sys
import os


class Game:
    run = True
    cancel = False
    path = os.path.expanduser('~\\Documents\\pokeTamago\\cfg')

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

        if os.path.exists(os.path.expanduser('~\\Documents\\pokeTamago\\cfg')):
            with open(f'{self.path}\\settings.json', 'r') as settings:
                data = json.load(settings)
                self.settings = data
        else:
            os.makedirs(self.path)
            self.save_settings()

        sg.theme(self.settings['theme'])
        f.poke_randomizer()


    def newGame(self, player):
        global index, frames, size

        poke = True
        new = False

        def portrait_thread():
            global index, frames
            while True:
                sleep(0.03)
                index = (index + 1) % frames
                if not poke:
                    break

        im = Image.open('src\\assets\\img\\poke\\default.gif')

        width, height = im.size
        frames = im.n_frames

        graph_width, graph_height = size = (170, 100)

        main_menu = sg.Window('', c.newGame(self,player), enable_close_attempted_event=True, finalize=True)
        
        main_menu['GRAPH'].draw_image('src\\assets\\img\\bg\\grassland-feild-day.png', location=(0, 0))
        main_menu['GRAPH2'].draw_image('src\\assets\\img\\bg\\grassland-feild-day.png', location=(0, 0))

        index = 1

        im.seek(index)

        location = (graph_width//2-width//2, graph_height//2-height//2)

        item = main_menu['GRAPH'].draw_image(data=f.image2data(im),location=location)

        thread = Thread(target=portrait_thread, daemon=True)
        if self.settings['portrait_anim']:
            thread.start()

        old_value = None
        name_value = None

        while True:
            event, values = main_menu.read(timeout=24)

            main_menu['poke'].bind('<Double-Button-1>', "-double click")
            main_menu['load'].bind('<Double-Button-1>', "-double click")

            match event:
                case sg.TIMEOUT_KEY:
                    try:
                        if values['poke']:
                            name = sub("[\\0-9](.*?)[\s]|[']", '', values['poke'][0])
                            im = Image.open(f'src\\assets\\img\\poke\\{name}.gif')

                            width, height = im.size
                            frames = im.n_frames

                            location = (graph_width//2-width//2, graph_height//2-height//2)

                            main_menu['type1'].update(
                                f'src\\assets\\img\\types\\{self.open_dex()[1][self.open_dex()[0].index(name)][0]}_Type_Icon.png')
                            if len(self.open_dex()[1][self.open_dex()[0].index(name)])==2:
                                main_menu['type2'].update(
                                    f'src\\assets\\img\\types\\{self.open_dex()[1][self.open_dex()[0].index(name)][1]}_Type_Icon.png')
                            else:
                                main_menu['type2'].update('src\\assets\\img\\types\\none.png')

                        elif values['load']:
                            path = os.path.expanduser('~\\Documents\\pokeTamago\\save')

                            with open(os.path.expanduser(f'{path}\\{values["load"][0]}.json'), 'r') as load:
                                data = json.load(load)

                            im = Image.open(f"{data['properties']['portrait']}")

                            width, height = im.size
                            frames = im.n_frames

                            location = (graph_width//2-width//2, graph_height//2-height//2)

                            leveling = f'level {data["properties"]["level"]}'
                            aliving = 'alive' if data["status"]["alive"] else 'fainted'
                            sleeping = 'sleep' if data["status"]["sleeping"] else 'awake'

                            main_menu['head1'].update(leveling.upper())
                            main_menu['head2'].update(aliving.upper())
                            main_menu['head3'].update(sleeping.upper())

                            main_menu['type3'].update(
                                f'src\\assets\\img\\types\\{data["properties"]["type"][0]}_Type_Icon.png')
                            if len(data['properties']['type'])==2:
                                main_menu['type4'].update(
                                    f'src\\assets\\img\\types\\{data["properties"]["type"][1]}_Type_Icon.png')
                            else:
                                main_menu['type4'].update('src\\assets\\img\\types\\none.png')

                        else:
                            im = Image.open('src\\assets\\img\\poke\\default.gif')

                            width, height = im.size
                            frames = im.n_frames

                            location = (graph_width//2-width//2, graph_height//2-height//2)

                            main_menu['type1'].update('src\\assets\\img\\types\\none.png')
                            main_menu['type2'].update('src\\assets\\img\\types\\none.png')
                            main_menu['type3'].update('src\\assets\\img\\types\\none.png')
                            main_menu['type4'].update('src\\assets\\img\\types\\none.png')
                            main_menu['group'].update('src\\assets\\img\\types\\none.png')
                            main_menu['nature'].update('src\\assets\\img\\types\\none.png')
                            main_menu['mood'].update('src\\assets\\img\\types\\none.png')
                            main_menu['xy'].update('src\\assets\\img\\types\\none.png')

                            main_menu['head1'].update('LEVEL 0')
                            main_menu['head2'].update('NONE')
                            main_menu['head3'].update('NONE')

                        im.seek(index)

                        item_new = main_menu['GRAPH' if new else 'GRAPH2'].draw_image(
                            data=f.image2data(im), location=location)

                        main_menu['GRAPH'].delete_figure(item)
                        main_menu['GRAPH2'].delete_figure(item)

                        item = item_new
                        
                    except EOFError:
                        pass

                    if not self.read_save():
                        main_menu['CONTINUE'].update(disabled=sg.BUTTON_DISABLED_MEANS_IGNORE,
                            image_data=f.image2data(None,True,'buttons\\disabled_button',0.65), 
                            button_color=('#363840', sg.theme_background_color()))
                        
                    self.settings['music_playing'] = values['_playing_']
                    self.settings['music_volume'] = values['_music_vol_']
                    self.settings['sound_volume'] = values['_sound_vol_']
                    self.settings['portrait_anim'] = values['_portrait_']
                    self.settings['scale'] = 0.5 if values['s1']==True else 1.5 if values['s3']==True else 1.0
                        
                    main_menu.refresh()

                case sg.WINDOW_CLOSE_ATTEMPTED_EVENT | 'EXIT':
                    event = c.pop_up(self,'','Are you sure you want to quit?')
                    
                    if event=='OK':
                        self.run = False
                        sys.exit()

                    if event=='CANCEL':
                        continue

                case 'NEW POKE':
                    new = True
                    main_menu['menu'].update(visible=False)
                    main_menu['choose'].update(visible=True)

                case 'RANDOM':
                    main_menu['-IN-'].update(value=generate())

                case 'CHOOSE' | 'poke-double click':
                    if search('^[A-Za-zÀ-ȕ0-9\\p{P}\\p{S}]{1,14}$', values['-IN-']) and values['-IN-'] not in self.read_save():
                        player.properties["name"] = values['-IN-']

                        if values['poke']:
                            name = sub("[\\0-9](.*?)[\s]|[']", '', values["poke"][0])
                            index = self.open_dex()[0].index(name)

                            player.properties['portrait'] = f'src\\assets\\img\\poke\\{name}.gif'
                            player.properties['type'] = self.open_dex()[1][index]
                            player.properties['xp_group'] = self.open_dex()[2][index]
                            player.properties['yield'] = self.open_dex()[3][index]

                            poke = False

                            break

                        else:
                            event = c.pop_up(self,'','You must choose a Pokemon!', True)

                            if event == 'OK':
                                continue          
                    else:
                        c.pop_up(self, '', 'Invalid name or this Pokemon is already exist!', True)

                case 'BACK1':
                    new = False
                    main_menu['menu'].update(visible=True)
                    main_menu['choose'].update(visible=False)
                    main_menu['poke'].update(set_to_index=[])

                case 'CONTINUE':
                    main_menu['menu'].update(visible=False)
                    main_menu['loading'].update(visible=True)

                case 'LOAD' | 'load+-double click-':
                    if not values['load']:
                        event = c.pop_up(self,'','You must choose a save file!',True)

                        if event == 'OK':
                            continue
                    else:
                        self.load_saves(player, values["load"][0])
                        player.offline_time()
                        poke = False
                        break

                case 'DELETE':
                    if not values["load"]:
                        event = c.pop_up(self,'','You must choose a save file!',True)

                        if event == 'OK':
                            continue
                    else:
                        event = c.pop_up(self,'','Are you sure you want to continue?')

                        if event == 'OK':
                            path = os.path.expanduser('~\\Documents\\pokeTamago\\save')
                            os.remove(f'{path}\\{values["load"][0]}.json')
                            self.read_save()
                            main_menu['load'].update(values=[x for x in self.read_save()])

                        if event == 'Cancel':
                            continue

                case 'BACK2':
                    main_menu['menu'].update(visible=True)
                    main_menu['loading'].update(visible=False)
                    main_menu['load'].update(set_to_index=[])

                case 'SETTINGS':
                    main_menu['menu'].update(visible=False)
                    main_menu['settings'].update(visible=True)

                    with open(f'{self.path}\\settings.json', 'r') as settings:
                        data = json.load(settings)
                        self.settings = data                  

                case 'DEFAULT':
                    self.settings = {
                        "theme": "TamagoDefault",
                        "background": "#516073",
                        "music": "music1",
                        "music_playing": True,
                        "music_volume": 100.0,
                        "sound_volume": 100.0,
                        "portrait_anim": True,
                        "scale": 1
                    }
                    self.save_settings()
                    os.execl(sys.executable, sys.executable, *sys.argv)

                case 'APPLY':
                    self.settings['theme'] = values['_theme_']
                    self.save_settings()
                    os.execl(sys.executable, sys.executable, *sys.argv)

                case 'BACK3':
                    event = c.pop_up(self,'','Are you sure you want to continue?\n' +
                        '(Your unapplied changes may be lost!)')

                    if event == 'OK':
                        path = os.path.expanduser('~\\Documents\\pokeTamago\\cfg')

                        with open(f'{path}\\settings.json', 'r') as settings:
                            data = json.load(settings)
                            self.settings = data

                        main_menu['_music_'].update(self.settings['music'])
                        main_menu['_theme_'].update(self.settings['theme'])
                        main_menu['menu'].update(visible=True)
                        main_menu['settings'].update(visible=False)

                    if event == 'CANCEL':
                        continue

            try:
                if main_menu.FindElementWithFocus() == main_menu['-IN-'] and values['-IN-'] == '--ENTER NAME--':
                    main_menu['-IN-'].update(value='')
                if main_menu.FindElementWithFocus() != main_menu['-IN-'] and values['-IN-'] == '':
                    main_menu['-IN-'].update(value='--ENTER NAME--')

            except KeyError:
                pass

            if old_value != values['search']:
                main_menu['poke'].update(
                    values=[f'{self.open_dex()[0].index(x)+1}. {x}' for x in self.open_dex()[0] if search(
                        f'(?i)(?:{values["search"]})', x)]
                    )
                old_value = values['search']

            if search('^(.{0,14})$', values['-IN-']):
                name_value = values['-IN-']
            else:
                main_menu['-IN-'].update(value=name_value)

            main_menu['_theme_txt_'].update(f"Current theme: {self.settings['theme']}")
            main_menu['_music_txt_'].update(f"Current music: {self.settings['music']}")
            main_menu['_playing_'].update(self.settings['music_playing'], text='Enabled' if self.settings['music_playing'] else 'Disabled')
            main_menu['_portrait_'].update(self.settings['portrait_anim'], text='Enabled' if self.settings['portrait_anim'] else 'Disabled')
            main_menu['m_value'].update(f'{int(self.settings["music_volume"])}')
            main_menu['_music_vol_'].update(f'{int(self.settings["music_volume"])}')
            main_menu['s_value'].update(f'{int(self.settings["sound_volume"])}')
            main_menu['_sound_vol_'].update(f'{int(self.settings["sound_volume"])}')

        main_menu.close()


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

        mainWindow = sg.Window('pokéTamago', c.mainGame(self, player), finalize=True,
            enable_close_attempted_event=True)

        mainWindow['GRAPH'].draw_image(f'{f.portrait_background(player)}', location=(0, 0))

        index = 1

        im.seek(index)

        location = (graph_width//2-width//2, graph_height//2-height//2)

        item = mainWindow['GRAPH'].draw_image(data=f.image2data(im),location=location)

        thread = Thread(target=portrait_thread, daemon=True)
        if self.settings['portrait_anim']:
            thread.start()

        while True:
            event, value = mainWindow.read(timeout=24)

            match event:
                case sg.TIMEOUT_KEY:
                    im.seek(index)
                    item_new = mainWindow['GRAPH'].draw_image(data=f.image2data(im), location=location)
                    mainWindow['GRAPH'].delete_figure(item)
                    item = item_new
                    mainWindow.refresh()

                case sg.WIN_CLOSED:
                    self.run = False
                    break

                case 'EAT':
                    c.eat_screen(self, player)

                case 'BATTLE':
                    pass

                case 'TRAINING':
                    c.train_screen(self, player)

                case 'PLAY':
                    c.play_screen(self, player)

                case 'SLEEP':
                    c.sleep_screen(self, player)
                    
                case 'MAIN MENU':
                    event = c.pop_up(self,'Quit','Are you sure you want to quit?')

                    if event == 'OK':
                        self.run = False
                        os.execl(sys.executable, sys.executable, *sys.argv)

                    if event == 'CANCLE':
                        continue

                case sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
                    event = c.pop_up(self,'Quit','Are you sure you want to quit?')

                    if event == 'OK':
                        self.run = False
                        break

                    if event == 'CANCLE':
                        continue

            if not player.status['alive']:
                c.death_screen(self, player)
            if player.status['sleeping']:
                c.sleep_screen(self, player)

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
        with open(f"{self.path}\\settings.json", 'w') as settings: 
            json.dump(self.settings, settings, indent=4)


    def open_dex(self):
        pokes = ([], [], [], [], [])

        with open('src\\cfg\\pokedex.json', 'r') as read_file:
            data = json.load(read_file)
            for poke in data:
                pokes[0].append(poke['name'])
                pokes[1].append(poke['type'])
                pokes[2].append(poke['xp_group'])
                pokes[3].append(poke['yield'])
                pokes[4].append(poke['nature'])

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
        path = os.path.expanduser('~\\Documents\\pokeTamago\\save')

        with open(os.path.expanduser(f'{path}\\{var}.json'), 'r') as load:
            data = json.load(load)

            player.properties = data['properties']
            player.base = data['base']
            player.condition = data['condition']
            player.status = data['status']