import PySimpleGUI as sg
import json
import sys
import os


def settings(self):
    status1 = 'Enabled' if self.settings['music_playing'] else 'Disabled'
    status2 = 'Enabled' if self.settings['portrait_anim'] else 'Disabled'

    listOfThemes = ['TamagoDefault', 'TamagoDark', 'TamagoLight']

    listOfMusic = ['music1', 'music2', 'music3']

    theme = [
        [sg.T(f"Current theme: {self.settings['theme']}", key='_theme_txt_')],
        [sg.Combo(listOfThemes, size=(25, 10), default_value=f"{self.settings['theme']}", key='_theme_')],
    ]

    sounds = [
        [sg.T(f"Current music: {self.settings['music']}", key='_music_txt_')],
        [sg.Combo(listOfMusic, size=(14, 0), default_value=self.settings['music'], key='_music_'),
        sg.Checkbox(text=status1, default=self.settings['music_playing'], key='_playing_')],
        [sg.T(f'Music')],
        [sg.Slider(orientation='h', disable_number_display=True,range=(0, 100), key='_music_vol_',
        default_value=self.settings['music_volume'])],
        [sg.T(f'Sound')],
        [sg.Slider(orientation='h', disable_number_display=True, range=(0, 100), key='_sound_vol_',
        default_value=self.settings['sound_volume'])]
    ]

    portrait = [
        [sg.T('Animated image:'), sg.Checkbox(text=status2, default=self.settings['portrait_anim'],
        p=((20, 0), (0, 0)), key='_portrait_')]
    ]

    layout = [
        [sg.Frame('Theme', theme, s=(215, 80))],
        [sg.Frame('Audio', sounds, s=(215, 200))],
        [sg.Frame('Portrait', portrait, s=(215, 55))],
        [sg.B('Default', p=((5, 0), (10, 5))), sg.B('Apply', p=((73, 0), (10, 5))),
        sg.B('Back', p=((10, 0), (10, 5)))]
    ]

    return layout


def settings_screen(self):
    OptWindow = sg.Window('Settings', settings(self), icon='data\\img\\gear.ico', grab_anywhere=True)

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

                event, values = sg.Window('error',[[sg.T('Are you sure you want to continue?\n' +
                    'Your unapplied changes may be lost!', justification='c')], [sg.B(
                    'OK', s=8, p=(10, 10)), sg.B('Cancel', s=8, p=(10, 10))]], keep_on_top=True,
                    icon='data\\img\\warning.ico', element_justification='c').read(close=True)

                if event == 'OK':
                    path = os.path.expanduser('~\\Documents\\pokeTamago\\cfg')
                    with open(f'{path}\\settings.json', 'r') as settings:
                        data = json.load(settings)
                        self.settings = data
                    break

                if event == sg.WIN_CLOSED or event == 'Cancel':
                    continue

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