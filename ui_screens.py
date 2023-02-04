from nickname_generator import generate
from threading import Thread
from random import randint
import PySimpleGUI as sg
import ui_layout as ui
from time import sleep
from PIL import Image
from re import sub, search
import funct as f
import sys
import os


def new_pokemon_screen(self, player):
    pokeName = sg.Window('Name', ui.newPoke(), icon='data\\img\\logo.ico', grab_anywhere=True)

    while True:
        event, values = pokeName.read(timeout=1000)

        match event:
            case sg.TIMEOUT_KEY:
                pokeName.refresh()

            case sg.WINDOW_CLOSED | 'Back':
                self.cancel = True
                break
            
            case 'Random':
                pokeName['-IN-'].update(value=generate())

            case 'Enter' | 'Submit':
                if 1 <= len(values['-IN-']) <= 14 and values['-IN-'] not in self.read_save():
                    player.properties["name"] = values['-IN-']
                    break
                else:
                    event, values = sg.Window('error',
                    [[sg.T('Invalid name or this Pokemon is already exist!')],
                    [sg.T('(The name cannot be longer than 14 characters)')],
                    [sg.B('OK', s=(10, 1), p=(10, 10), bind_return_key=True,focus=True)]],
                    keep_on_top=True, auto_close=True, auto_close_duration=3, element_justification='c',
                    icon='data\\img\\warning.ico').read(close=True)

    pokeName.close()


def choose_pokemon(self, player):
    pokeChooseWin = sg.Window('Choose', ui.choosePoke(self), icon='data\\img\\pokeball.ico')

    while True:
        event, values = pokeChooseWin.read(timeout=100)
        pokeChooseWin["poke"].bind('<Double-Button-1>', "+-double click-")

        match event:
            case sg.WINDOW_CLOSED | 'Back':
                player.properties['name'] = ""
                break

            case 'Choose' | 'poke+-double click-':
                index = self.open_dex()[0].index(f'{values["poke"][0]}')
                name = sub("\s|[']", '', values["poke"][0])
                player.properties['portrait'] = f'data\\img\\poke\\{name}.gif'
                player.properties['type'] = self.open_dex()[1][index]
                player.properties['xp_group'] = self.open_dex()[2][index]
                player.properties['yield'] = self.open_dex()[3][index]
                self.cancel = True
                break

    pokeChooseWin.close()


def loading_screen(self, player):
    loadScreen = sg.Window('Load', ui.load(self), icon='data\\img\\load.ico', size=(214,333))

    while True:
        event, values = loadScreen.read()  
        loadScreen["load"].bind('<Double-Button-1>', "+-double click-")

        match event:
            case sg.WINDOW_CLOSED | 'Back':
                break

            case 'Load' | 'load+-double click-':
                if not values["load"]:
                    sg.Popup('You must choose a save file!', title='error', keep_on_top=True,
                    auto_close=True, auto_close_duration=3, icon='data\\img\\warning.ico')
                else:
                    self.load_saves(player, values["load"][0])
                    break

            case 'Delete':
                if not values["load"]:
                    sg.Popup('You must choose a save file!', title='error', keep_on_top=True,
                    auto_close=True, auto_close_duration=3, icon='data\\img\\warning.ico')
                else:
                    path = os.path.expanduser('~\\Documents\\pokeTamago\\save')
                    os.remove(f'{path}\\{values["load"][0]}.json')
                    self.read_save()
                    loadScreen['load'].update(values=[x for x in self.read_save()])

    loadScreen.close()


def settings_screen(self):
    OptWindow = sg.Window('Settings', ui.settings(self), icon='data\\img\\gear.ico', grab_anywhere=True)

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

        OptWindow['_playing_'].update(text='Enabled' if self.settings['music_playing'] is True else 'Disabled')
        OptWindow['_portrait_'].update(text='Enabled' if self.settings['portrait_anim'] is True else 'Disabled')
        OptWindow['_theme_txt_'].update(f"Current theme: {self.settings['theme']}")
        OptWindow['_music_txt_'].update(f"Current music: {self.settings['music']}")

    OptWindow.close()


def death_screen(self, player):

    if not player.status["revive"]:
        deathWindow = sg.Window('Passing', ui.dead(player)[0], icon='data\\img\\death.ico',
        element_justification="center")
    else:
        deathWindow = sg.Window('Revive', ui.dead(player)[1], icon='data\\img\\death.ico',
        element_justification="center")

    while True:
        event, value = deathWindow.read(timeout=150)

        match event:
            case sg.WIN_CLOSED | 'Exit':
                self.run = False
                sys.exit()

            case 'r':
                player.status['revive'] = True
                player.status['revive_time'] = 604800

            case 'l':
                os.remove(os.path.expanduser(f'~\\Documents\\pokeTamago\\save\\{player.properties["name"]}.json'))
                self.run = False
                os.execl(sys.executable, sys.executable, *sys.argv)

        if player.status['revive'] and player.status['revive_time'] == 0:
            player.condition['health'] = player.condition['MaxHP']
            player.condition['bored'] = 0
            player.condition['food'] = 100
            player.condition['exhausted'] = 0
            player.status['alive'] = True
            player.status['revive'] = False
            break

        if player.status["revive"]:
            deathWindow['image'].UpdateAnimation('data\\img\\revive.gif', time_between_frames=150)
            deathWindow['text1'].update('Your pet is about to begin a new life.')
            deathWindow['text2'].update(f'The process will take {f.time_counter(player.status["revive_time"])}.')
            deathWindow['r'].update(disabled=True)
            deathWindow['l'].update(disabled=True)
        else:
            deathWindow['image'].UpdateAnimation('data\\img\\death.gif', time_between_frames=150)

    deathWindow.close()


def train_screen(self, player):
    global index1, index2, index3, frames1, frames2, frames3, size

    train = True

    def portrait_thread():
        global index1, index2, index3, frames1, frames2, frames3
        while True:
            sleep(0.03)
            index1 = (index1 + 1) % frames1
            if player.status['training'] == True:
                index2 = (index2 + 1) % frames2
                index3 = (index3 + 1) % frames3
            if not train:
                break

    im1 = Image.open(player.properties['portrait'])
    im2 = Image.open('data\\img\\sweat1.gif')
    im3 = Image.open('data\\img\\sweat2.gif')

    width1, height1 = im1.size
    width2, height2 = im2.size
    width3, height3 = im3.size

    frames1 = im1.n_frames
    frames2 = im2.n_frames
    frames3 = im3.n_frames

    graph_width, graph_height = size = (300, 260)

    trainWindow = sg.Window('Training', ui.training(player), finalize=True, size=(320, 365),
    icon='data\\img\\gym.ico', element_justification="c")

    trainWindow['train_graph'].draw_image('data\\img\\gym_training.png', location=(0, 0))

    index1 = 1
    index2 = 1
    index3 = 1

    im1.seek(index1)
    im2.seek(index2)
    im3.seek(index3)

    location1 = (graph_width//2-width1//2, graph_height//1.4-height1)
    location2 = ((graph_width//2-width2//2)+60, graph_height//1.4-height1//1.5)
    location3 = ((graph_width//2-width2//2)-60, graph_height//1.4-height1//1.5)

    item1 = trainWindow['train_graph'].draw_image(data=f.image_to_data(im1), location=location1)
    item2 = trainWindow['train_graph'].draw_image(data=f.image_to_data(im2), location=location2)
    item3 = trainWindow['train_graph'].draw_image( data=f.image_to_data(im3), location=location3)

    thread = Thread(target=portrait_thread, daemon=True)
    if self.settings['portrait_anim']:
        thread.start()

    while True:
        event, value = trainWindow.read(timeout=25)

        match event:
            case sg.TIMEOUT_KEY:
                trainWindow['train_graph'].delete_figure(item2)
                trainWindow['train_graph'].delete_figure(item3)  

                im1.seek(index1)

                item_new1 = trainWindow['train_graph'].draw_image(data=f.image_to_data(im1),
                location=location1)

                trainWindow['train_graph'].delete_figure(item1)

                item1 = item_new1

                if player.status['training'] == True:
                    im2.seek(index2)
                    im3.seek(index3)
                    item_new2 = trainWindow['train_graph'].draw_image(data=f.image_to_data(im2),
                    location=location2)
                    item_new3 = trainWindow['train_graph'].draw_image(data=f.image_to_data(im3),
                    location=location3)              
                    item2 = item_new2
                    item3 = item_new3

                trainWindow.refresh()

            case sg.WIN_CLOSED | 'Back':
                train = False
                break

            case 'begin':
                player.training()

        if player.status['training'] == True:
            trainWindow['train'].update('Your pokemon is already trained!\n' +
            f'It needs to rest for about {f.time_counter(player.status["training_time"])}')
            trainWindow['begin'].update(disabled=True)

            if player.status['training_time'] == 0:
                player.status['training'] = False
                trainWindow['train'].update('Your pokemon is ready for training!\n'
                + 'Please, be gentle with it!')
                trainWindow['begin'].update(disabled=False)

    trainWindow.close()


def sleep_screen(self, player):
    global index1, index2, frames1, frames2, size

    sleeping = True

    def portrait_thread():
        global index1, index2, frames1, frames2
        while True:
            sleep(0.03)
            index1 = (index1 + 1) % frames1
            index2 = (index2 + 1) % frames2
            if not sleeping:
                break

    im1 = Image.open(player.properties['portrait'])
    im2 = Image.open('data\\img\\sleep.gif')

    width1, height1 = im1.size
    width2, height2 = im2.size

    frames1 = im1.n_frames
    frames2 = im2.n_frames

    graph_width, graph_height = size = (300, 260)

    sleepWindow = sg.Window('Sleeping', ui.sleeping(player), finalize=True, size=(320, 375),
    element_justification="c", icon='data\\img\\sleep.ico')

    sleepWindow['sleep_graph'].draw_image('data\\img\\room_sleeping.png', location=(0, 0))

    index1 = 1
    index2 = 1

    im1.seek(index1)
    im2.seek(index2)

    location1 = (graph_width//2-width1//2, graph_height//1.65-height1//1.65)
    location2 = (graph_width//2-width1//2, graph_height//2-(height2-10))

    item1 = sleepWindow['sleep_graph'].draw_image(data=f.image_to_data(im1), location=location1)
    item2 = sleepWindow['sleep_graph'].draw_image(data=f.image_to_data(im2), location=location2)

    thread = Thread(target=portrait_thread, daemon=True)
    if self.settings['portrait_anim']:
        thread.start()

    while True:
        event, value = sleepWindow.read(timeout=30)
        
        match event:
            case sg.TIMEOUT_KEY:
                im1.seek(index1)
                im2.seek(index2)

                item_new1 = sleepWindow['sleep_graph'].draw_image(data=f.image_to_data(im1),
                location=location1)
                item_new2 = sleepWindow['sleep_graph'].draw_image(data=f.image_to_data(im2),
                location=location2)

                sleepWindow['sleep_graph'].delete_figure(item1)
                sleepWindow['sleep_graph'].delete_figure(item2)

                item1 = item_new1
                item2 = item_new2

                sleepWindow.refresh()

            case sg.WIN_CLOSED:
                self.run = False
                sys.exit()

            case 'Main Menu':
                self.run = False
                os.execl(sys.executable, sys.executable, *sys.argv)

        if player.status['sleeping'] and player.status['sleep_time'] == 0:
            player.status['sleeping'] = False
            break

        sleepWindow['text'].update('Shhh!!! Your pet is sleeping now.\n' + 
        f'Let it rest for about {f.time_counter(player.status["sleep_time"])}.')

    sleepWindow.close()


def eat_screen(self, player):
    global index1, index2, frames1, frames2, size

    eating = True

    def portrait_thread():
            global index1, index2, frames1, frames2
            while True:
                sleep(0.03)
                index1 = (index1 + 1) % frames1
                if player.status['eating'] == True:
                    index2 = (index2 + 1) % frames2
                if not eating:
                    break

    im1 = Image.open(player.properties['portrait'])
    im2 = Image.open('data\\img\\Frame_1.gif')

    width1, height1 = im1.size
    width2, height2 = im2.size

    frames1 = im1.n_frames
    frames2 = im2.n_frames

    graph_width, graph_height = size = (300, 260)

    eatWindow = sg.Window('Eating', ui.eating(), finalize=True, size=(320, 375),
    element_justification="c", icon='data\\img\\eat.ico')

    eatWindow['eat_graph'].draw_image('data\\img\\kitchen_eating.png', location=(0, 0))

    index1 = 1
    index2 = 1

    im1.seek(index1)
    im2.seek(index2)

    location1 = (graph_width//2-width1//2, graph_height//1.5-height1)
    location2 = (graph_width//2-width2//2, graph_height//1.5-(height2+(height1//2)))

    item1 = eatWindow['eat_graph'].draw_image(data=f.image_to_data(im1), location=location1)
    item2 = eatWindow['eat_graph'].draw_image(data=f.image_to_data(im2), location=location2)

    thread = Thread(target=portrait_thread, daemon=True)
    if self.settings['portrait_anim']:
        thread.start()

    while True:
        event, value = eatWindow.read(timeout=30)

        match event:
            case sg.TIMEOUT_KEY:
                eatWindow['eat_graph'].delete_figure(item2)

                im1.seek(index1)
                
                item_new1 = eatWindow['eat_graph'].draw_image(data=f.image_to_data(im1),
                location=location1)

                eatWindow['eat_graph'].delete_figure(item1)

                item1 = item_new1

                if player.status['eating'] == True:
                    im2.seek(index2)
                    item_new2 = eatWindow['eat_graph'].draw_image(data=f.image_to_data(im2),
                    location=location2)
                    item2 = item_new2

                eatWindow.refresh()

            case sg.WINDOW_CLOSED | 'Back':
                eating = False
                break

            case 'feed':
                player.eat()

        if player.status['eating']:
            eatWindow['text1'].update(visible=False)
            eatWindow['text3'].update(visible=True)
            eatWindow['feed'].update(disabled=True)
            if player.status['eat_time'] == 0:
                player.status['eating'] = False
                eatWindow['text1'].update(visible=True)
                eatWindow['text3'].update(visible=False)
                eatWindow['feed'].update(disabled=False)

    eatWindow.close()
