import sys
import os
from re import search, sub
import funct as f
import ui_layout as ui
import PySimpleGUI as sg


def new_pokemon_screen(self, player):
    pokeName = sg.Window('Name', ui.newPoke(), icon='Data\\img\\logo.ico', grab_anywhere=True)

    while True:
        event, values = pokeName.read()
        match event:
            case sg.WINDOW_CLOSED | 'Back':
                break
            case 'Enter' | 'Submit':
                self.read_save()
                if search('^[A-Za-z0-9]{1,14}$', values['-IN-']) and values['-IN-'] not in self.read_save():
                    player.properties["name"] = values['-IN-']
                    break
                else:
                    event, values = sg.Window('error', [[sg.T('Invalid name or this Pokemon is already exist!')],
                    [sg.T('(The name cannot be longer than 14 characters and cannot contain any special character.)')],
                    [sg.B('OK', s=(10,1), p=(10,10))]], keep_on_top=True, auto_close=True, auto_close_duration=3,
                    element_justification='c', icon='Data\\img\\warning.ico').read(close=True)

    pokeName.close()


def choose_pokemon(self, player):
    pokeChooseWin = sg.Window('Choose', ui.choosePoke(self),
                              icon='Data\\img\\pokeball.ico')

    while True:
        event, values = pokeChooseWin.read()
        match event:
            case sg.WINDOW_CLOSED | 'Back':
                break
            case 'Choose' | 'Submit':
                index = self.open_dex()[0].index(f'{values["poke"][0]}')
                name = sub("\s|[']", '', values["poke"][0])
                player.properties['portrait'] = f'Data\\img\\poke\\{name}.gif'
                player.properties['type'] = self.open_dex()[1][index]
                break
    pokeChooseWin.close()


def loading_screen(self, player):
    loadScreen = sg.Window('Load', ui.load(self), icon='Data\\img\\load.ico')

    while True:
        event, values = loadScreen.read()
        match event:
            case sg.WINDOW_CLOSED | 'Back':
                break
            case 'Load' | 'Submit':
                if not values["load"]:
                    sg.Popup('You must choose a save file!', title='error', keep_on_top=True,
                             auto_close=True, auto_close_duration=3, icon='Data\\img\\warning.ico')
                else:
                    player.load_saves(player, values["load"][0])
                    break
            case 'Delete':
                if not values["load"]:
                    sg.Popup('You must choose a save file!', title='error', keep_on_top=True,
                             auto_close=True, auto_close_duration=3, icon='Data\\img\\warning.ico')
                else:
                    os.remove(f'Data\\save\\{values["load"][0]}.json')
                    self.read_save()
                    loadScreen['load'].update(values=[x for x in self.read_save()])

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
            case sg.WIN_CLOSED | 'Back':
                f.save_settings(self)
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
        deathWindow = sg.Window(
            'Passing', ui.dead1(), icon='Data\\img\\death.ico', element_justification="center")
    else:
        deathWindow = sg.Window(
            'Revive', ui.dead2(player), icon='Data\\img\\death.ico', element_justification="center")

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
            player.condition['health'] = player.stats['MaxHP']
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


def sleep_screen(self, player):
    sleepWindow = sg.Window(
        'Sleeping', ui.sleeping(player), icon='Data\\img\\sleep.ico', element_justification="center")

    while True:
        event, value = sleepWindow.read(timeout=150)
        if (event == sg.WIN_CLOSED) or (event == 'Exit'):
            self.autosave()
            self.run = False
            sys.exit()
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
