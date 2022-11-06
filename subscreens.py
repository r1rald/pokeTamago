import sys
import os
import funct as f
import layouts as ui
import PySimpleGUI as sg
import themes


def new_pokemon_screen(self):
    pokeName = sg.Window(
        'Name', ui.newPoke(), icon='Data\\img\\logo.ico', grab_anywhere=True)

    while True:
        event, values = pokeName.read()
        match event:
            case sg.WINDOW_CLOSED | 'Back':
                break
            case 'Enter' | 'Submit':
                f.saves.clear()
                f.read_save()
        if values['-IN-'] in f.saves:
            sg.Popup('This Pokemon is already exist!', title='error', keep_on_top=True,
                     auto_close=True, auto_close_duration=3, icon='Data\\img\\warning.ico')
        elif values['-IN-'] == '':
            sg.Popup('You must give a name to your Pokemon!', title='error', keep_on_top=True,
                     auto_close=True, auto_close_duration=3, icon='Data\\img\\warning.ico')
        elif len(values['-IN-']) > 14:
            sg.Popup('Please try a shorter name!', title='error', keep_on_top=True,
                     auto_close=True, auto_close_duration=3, icon='Data\\img\\warning.ico')
        else:
            self.stats["name"] = values['-IN-']
            break
    pokeName.close()


def choose_pokemon(self):
    pokeChooseWin = sg.Window('Choose', ui.choosePoke(),
                              icon='Data\\img\\pokeball.ico')

    while True:
        event, values = pokeChooseWin.read()
        match event:
            case sg.WINDOW_CLOSED | 'Back':
                break
            case 'Choose' | 'Submit':
                index = f.pokes.index(f'{values["poke"][0]}')
                if ' ' in values["poke"][0]:
                    name = values["poke"][0].replace(' ', '')
                elif "'" in values["poke"][0]:
                    name = values["poke"][0].replace("'", '')
                else:
                    name = values["poke"][0]
                self.stats['portrait'] = f'Data\\img\\poke\\{name}.gif'
                self.stats['type'] = f.types[index]
                break
    pokeChooseWin.close()


def loading_screen(self):
    loadScreen = sg.Window('Load', ui.load(), icon='Data\\img\\load.ico')

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
                    f.load_saves(self, values["load"][0])
                    break
            case 'Delete':
                if not values["load"]:
                    sg.Popup('You must choose a save file!', title='error', keep_on_top=True,
                             auto_close=True, auto_close_duration=3, icon='Data\\img\\warning.ico')
                else:
                    os.remove(f'Data\\save\\{values["load"][0]}.json')
                    f.saves.clear()
                    f.read_save()
                    loadScreen['load'].update(values=[x for x in f.saves])
    loadScreen.close()


def option_screen(self):
    OptWindow = sg.Window(
        'Options', ui.options(self), icon='Data\\img\\gear.ico', grab_anywhere=True)

    while True:
        event, values = OptWindow.read(timeout=100)
        match event:
            case sg.TIMEOUT_KEY:
                self.settings['music'] = values['_music_']
                self.settings['music_playing'] = values['_playing_']
                self.settings['music_volume'] = values['_music_vol_']
                self.settings['sound_volume'] = values['_sound_vol_']
                self.settings['effects_volume'] = values['_effects_vol_']
            case sg.WIN_CLOSED | 'Back':
                f.save_settings(self)
                break
            case 'Apply':
                self.settings['theme'] = values['_theme_']
                f.save_settings(self)
                os.execl(sys.executable, sys.executable, *sys.argv)
                

        OptWindow['_theme_txt_'].update(f"Current theme: {self.settings['theme']}")
        OptWindow['_music_txt_'].update(f"Current music: {self.settings['music']}")

    OptWindow.close()


def death_screen(self):
    if not self.status["revive"]:
        deathWindow = sg.Window(
            'Passing', ui.dead1(), icon='Data\\img\\death.ico', element_justification="center")
    else:
        deathWindow = sg.Window(
            'Revive', ui.dead2(self), icon='Data\\img\\death.ico', element_justification="center")

    while True:
        event, value = deathWindow.read(timeout=150)
        if (event == sg.WIN_CLOSED) or (event == 'Exit'):
            self.run = False
            sys.exit()
        if (event == 'r'):
            self.status['revive'] = True
            self.status['revive_time'] = 604800
        if (event == 'l'):
            os.remove(f'Data\\save\\{self.stats["name"]}.json')
            self.run = False
            sys.exit()
        if self.status['revive'] and self.status['revive_time'] == 0:
            self.condition['health'] = self.stats['MaxHP']
            self.condition['bored'] = 0
            self.condition['food'] = 100
            self.condition['exhausted'] = 0
            self.status['alive'] = True
            self.status['revive'] = False
            break

        if not self.status["revive"]:
            deathWindow['image'].UpdateAnimation(
                'Data\\img\\death.gif', time_between_frames=150)
        if self.status["revive"]:
            deathWindow['image'].UpdateAnimation(
                'Data\\img\\revive.gif', time_between_frames=150)
            deathWindow['text1'].update(
                'Your pet is about to begin a new life.')
            deathWindow['text2'].update(
                f'The process will take {f.time_counter(self.status["revive_time"])}.')
            deathWindow['r'].update(disabled=True)
            deathWindow['l'].update(disabled=True)

    deathWindow.close()


def sleep_screen(self):
    sleepWindow = sg.Window(
        'Sleeping', ui.sleeping(self), icon='Data\\img\\sleep.ico', element_justification="center")

    while True:
        event, value = sleepWindow.read(timeout=150)
        if (event == sg.WIN_CLOSED) or (event == 'Exit'):
            self.autosave()
            self.run = False
            sys.exit()
        if self.status['sleeping'] and self.status['sleep_time'] == 0:
            self.status['sleeping'] = False
            break

        sleepWindow['image'].UpdateAnimation(
            'Data\\img\\sleep.gif', time_between_frames=150)
        sleepWindow['text'].update(
            f'Let it rest for about {f.time_counter(self.status["sleep_time"])}.')

    sleepWindow.close()


def eat_screen(self):
    eatWindow = sg.Window(
        'Eating', ui.eating(), icon='Data\\img\\eat.ico', element_justification="center")

    while True:
        event, value = eatWindow.read(timeout=150)
        if (event == sg.WIN_CLOSED) or (event == 'Back'):
            break
        if (event == 'snack'):
            portion -= 1
            if self.condition['food'] <= 90 and f.chance(2):
                self.condition['food'] += 10
                ui.gif_update = 'snack'
            else:
                ui.gif_update = 'eat_miss'
        if (event == 'meal'):
            portion -= 1
            if self.condition['food'] <= 75 and f.chance(3):
                self.condition['food'] += 25
                ui.gif_update = 'meal'
            else:
                ui.gif_update = 'eat_miss'

        eatWindow['image'].UpdateAnimation(
            f'Data\\img\\{ui.gif_update}.gif', time_between_frames=150)
        eatWindow['text1'].update(f'You have {ui.portion} portions.')

        if ui.portion == 0:
            eatWindow['text2'].update(visible=True)
        if self.condition['food'] > 75:
            eatWindow['meal'].update(disabled=True)
            if self.condition['food'] > 90:
                eatWindow['text3'].update(visible=True)
                eatWindow['snack'].update(disabled=True)

    self.status['eating'] = False
    eatWindow.close()
