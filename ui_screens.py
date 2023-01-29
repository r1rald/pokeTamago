from threading import Thread
from re import search, sub
import PySimpleGUI as sg
import ui_layout as ui
from time import sleep
from PIL import Image
import funct as f
import sys
import os


def new_pokemon_screen(self, player):
    pokeName = sg.Window('Name', ui.newPoke(),
                         icon='Data\\img\\logo.ico', grab_anywhere=True)

    while True:
        event, values = pokeName.read()
        match event:
            case sg.WINDOW_CLOSED | 'Back':
                self.cancel = True
                break
            case 'Enter' | 'Submit':
                self.read_save()
                if 1 <= len(values['-IN-']) <= 14 and values['-IN-'] not in self.read_save():
                    player.properties["name"] = values['-IN-']
                    break
                else:
                    event, values = sg.Window('error', [[sg.T('Invalid name or this Pokemon is already exist!')],
                                                        [sg.T(
                                                            '(The name cannot be longer than 14 characters)')],
                                                        [sg.B('OK', s=(10, 1), p=(10, 10), bind_return_key=True,
                                                              focus=True)]], keep_on_top=True, auto_close=True,
                                              auto_close_duration=3, element_justification='c',
                                              icon='Data\\img\\warning.ico').read(close=True)
    pokeName.close()


def choose_pokemon(self, player):
    pokeChooseWin = sg.Window('Choose', ui.choosePoke(self),
                              icon='Data\\img\\pokeball.ico')

    while True:
        event, values = pokeChooseWin.read()
        pokeChooseWin["poke"].bind('<Double-Button-1>', "+-double click-")
        match event:
            case sg.WINDOW_CLOSED | 'Back':
                player.properties['name'] = ""
                break
            case 'Choose' | 'poke+-double click-':
                index = self.open_dex()[0].index(f'{values["poke"][0]}')
                name = sub("\s|[']", '', values["poke"][0])
                player.properties['portrait'] = f'Data\\img\\poke\\{name}.gif'
                player.properties['type'] = self.open_dex()[1][index]
                player.properties['xp_group'] = self.open_dex()[2][index]
                player.properties['yield'] = self.open_dex()[3][index]
                self.cancel = True
                break

    pokeChooseWin.close()


def loading_screen(self, player):
    loadScreen = sg.Window('Load', ui.load(self), icon='Data\\img\\load.ico')

    while True:
        event, values = loadScreen.read()
        loadScreen["load"].bind('<Double-Button-1>', "+-double click-")
        match event:
            case sg.WINDOW_CLOSED | 'Back':
                break
            case 'Load' | 'load+-double click-':
                if not values["load"]:
                    sg.Popup('You must choose a save file!', title='error', keep_on_top=True,
                             auto_close=True, auto_close_duration=3, icon='Data\\img\\warning.ico')
                else:
                    self.load_saves(player, values["load"][0])
                    break
            case 'Delete':
                if not values["load"]:
                    sg.Popup('You must choose a save file!', title='error', keep_on_top=True,
                             auto_close=True, auto_close_duration=3, icon='Data\\img\\warning.ico')
                else:
                    os.remove(f'Data\\save\\{values["load"][0]}.json')
                    self.read_save()
                    loadScreen['load'].update(
                        values=[x for x in self.read_save()])

    loadScreen.close()


def settings_screen(self):
    OptWindow = sg.Window(
        'Settings', ui.settings(self), icon='Data\\img\\gear.ico', grab_anywhere=True)

    while True:
        event, values = OptWindow.read(timeout=100)
        match event:
            case sg.TIMEOUT_KEY:
                self.settings['music'] = values['_music_']
                self.settings['music_playing'] = values['_playing_']
                self.settings['music_volume'] = values['_music_vol_']
                self.settings['sound_volume'] = values['_sound_vol_']
                self.settings['portrait_anim'] = values['_portrait_']
                OptWindow.refresh()
            case 'Default':
                self.settings = {
                    "theme": "TamagoDefault",
                    "background": "#516073",
                    "music": "music1",
                    "music_playing": True,
                    "music_volume": 100.0,
                    "sound_volume": 100.0,
                    "portrait_anim": True
                }
                self.save_settings()
                os.execl(sys.executable, sys.executable, *sys.argv)
            case sg.WIN_CLOSED | 'Back':
                break
            case 'Apply':
                self.settings['theme'] = values['_theme_']
                self.save_settings()
                os.execl(sys.executable, sys.executable, *sys.argv)

        OptWindow['_playing_'].update(
            text='Enabled' if self.settings['music_playing'] is True else 'Disabled')
        OptWindow['_portrait_'].update(
            text='Enabled' if self.settings['portrait_anim'] is True else 'Disabled')
        OptWindow['_theme_txt_'].update(
            f"Current theme: {self.settings['theme']}")
        OptWindow['_music_txt_'].update(
            f"Current music: {self.settings['music']}")

    OptWindow.close()


def death_screen(self, player):
    if not player.status["revive"]:
        deathWindow = sg.Window(
            'Passing', ui.dead(player)[0], icon='Data\\img\\death.ico', element_justification="center")
    else:
        deathWindow = sg.Window(
            'Revive', ui.dead(player)[1], icon='Data\\img\\death.ico', element_justification="center")

    while True:
        event, value = deathWindow.read(timeout=150)
        if (event == sg.WIN_CLOSED) or (event == 'Exit'):
            self.run = False
            sys.exit()
        if (event == 'r'):
            player.status['revive'] = True
            player.status['revive_time'] = 604800
        if (event == 'l'):
            os.remove(f'Data\\save\\{self.stats["name"]}.json')
            self.run = False
            sys.exit()
        if player.status['revive'] and player.status['revive_time'] == 0:
            player.condition['health'] = player.condition['MaxHP']
            player.condition['bored'] = 0
            player.condition['food'] = 100
            player.condition['exhausted'] = 0
            player.status['alive'] = True
            player.status['revive'] = False
            break

        if not player.status["revive"]:
            deathWindow['image'].UpdateAnimation(
                'Data\\img\\death.gif', time_between_frames=150)
        if player.status["revive"]:
            deathWindow['image'].UpdateAnimation(
                'Data\\img\\revive.gif', time_between_frames=150)
            deathWindow['text1'].update(
                'Your pet is about to begin a new life.')
            deathWindow['text2'].update(
                f'The process will take {f.time_counter(player.status["revive_time"])}.')
            deathWindow['r'].update(disabled=True)
            deathWindow['l'].update(disabled=True)

    deathWindow.close()


def train_screen(self, player):
    global index1, index2, index3, frames1, frames2, frames3, size

    train = True

    def portrait_thread():
        global index1, index2, index3, frames1, frames2, frames3
        while True:
            sleep(0.03)
            index1 = (index1 + 1) % frames1
            index2 = (index2 + 1) % frames2
            index3 = (index3 + 1) % frames3
            if not train:
                break

    im1 = Image.open(player.properties['portrait'])
    im2 = Image.open('Data\\img\\sweat1.gif')
    im3 = Image.open('Data\\img\\sweat2.gif')

    width1, height1 = im1.size
    width2, height2 = im2.size
    width3, height3 = im3.size

    frames1 = im1.n_frames
    frames2 = im2.n_frames
    frames3 = im3.n_frames

    graph_width, graph_height = size = (300, 260)

    trainWindow = sg.Window('Training', ui.training(player), icon='Data\\img\\gym.ico', element_justification="c",
                            size=(320, 365), finalize=True)

    trainWindow['train_graph'].draw_image(
        'Data\\img\\gym_training.png', location=(0, 0))

    index1 = 0 if self.settings['portrait_anim'] else 10
    index2 = 0 if self.settings['portrait_anim'] else 5
    index3 = 0 if self.settings['portrait_anim'] else 5
    im1.seek(index1)
    im2.seek(index2)
    im3.seek(index3)
    location1 = (graph_width//2-width1//2, graph_height//1.65-height1//1.65)
    location2 = (graph_width//1.25-width2//1.25,
                 graph_height//1.75-height2//1.75)
    location3 = (graph_width//4.25-width3//4.25,
                 graph_height//1.75-height3//1.75)
    item1 = trainWindow['train_graph'].draw_image(
        data=f.image_to_data(im1), location=location1)
    item2 = trainWindow['train_graph'].draw_image(
        data=f.image_to_data(im2), location=location2)
    item3 = trainWindow['train_graph'].draw_image(
        data=f.image_to_data(im3), location=location3)

    thread = Thread(target=portrait_thread, daemon=True)
    if self.settings['portrait_anim']:
        thread.start()

    while True:
        event, value = trainWindow.read(timeout=25)
        match event:
            case sg.TIMEOUT_KEY:
                im1.seek(index1)
                im2.seek(index2)
                im3.seek(index3)
                item_new1 = trainWindow['train_graph'].draw_image(
                    data=f.image_to_data(im1), location=location1)
                item_new2 = trainWindow['train_graph'].draw_image(
                    data=f.image_to_data(im2), location=location2)
                item_new3 = trainWindow['train_graph'].draw_image(
                    data=f.image_to_data(im3), location=location3)
                trainWindow['train_graph'].delete_figure(item1)
                trainWindow['train_graph'].delete_figure(item2)
                trainWindow['train_graph'].delete_figure(item3)
                item1 = item_new1
                item2 = item_new2
                item3 = item_new3
                trainWindow.refresh()

            case sg.WIN_CLOSED | 'Back':
                train = False
                player.status['training'] = False
                break

            case "Let's begin":
                player.training()

        if player.status['training_time'] > 0:
            trainWindow['train'].update('Your pokemon is already trained!\n' +
                                        f'It needs to rest for about {f.time_counter(player.status["training_time"])}')

    trainWindow.close()


def sleep_screen(self, player):
    sleepWindow = sg.Window(
        'Sleeping', ui.sleeping(player), icon='Data\\img\\sleep.ico', element_justification="center")

    while True:
        event, value = sleepWindow.read(timeout=150)
        if event == sg.WIN_CLOSED:
            self.run = False
            sys.exit()
        if event == 'Main Menu':
            self.run = False
            os.execl(sys.executable, sys.executable, *sys.argv)
        if player.status['sleeping'] and player.status['sleep_time'] == 0:
            player.status['sleeping'] = False
            break

        sleepWindow['image'].UpdateAnimation(
            'Data\\img\\sleep.gif', time_between_frames=150)
        sleepWindow['text'].update(
            f'Let it rest for about {f.time_counter(player.status["sleep_time"])}.')

    sleepWindow.close()


def eat_screen(player):
    eatWindow = sg.Window(
        'Eating', ui.eating(), icon='Data\\img\\eat.ico', element_justification="center")

    while True:
        event, value = eatWindow.read(timeout=150)
        if (event == sg.WIN_CLOSED) or (event == 'Back'):
            break
        if (event == 'snack'):
            portion -= 1
            if player.condition['food'] <= 90 and f.chance(2):
                player.condition['food'] += 10
                ui.gif_update = 'snack'
            else:
                ui.gif_update = 'eat_miss'
        if (event == 'meal'):
            portion -= 1
            if player.condition['food'] <= 75 and f.chance(3):
                player.condition['food'] += 25
                ui.gif_update = 'meal'
            else:
                ui.gif_update = 'eat_miss'

        eatWindow['image'].UpdateAnimation(
            f'Data\\img\\{ui.gif_update}.gif', time_between_frames=150)
        eatWindow['text1'].update(f'You have {ui.portion} portions.')

        if ui.portion == 0:
            eatWindow['text2'].update(visible=True)
        if player.condition['food'] > 75:
            eatWindow['meal'].update(disabled=True)
            if player.condition['food'] > 90:
                eatWindow['text3'].update(visible=True)
                eatWindow['snack'].update(disabled=True)

    player.status['eating'] = False
    eatWindow.close()
