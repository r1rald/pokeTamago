import src.components as c
import PySimpleGUI as sg
import json
import sys
import os


def settings(self):
    match self.settings['theme']:

        case "TamagoDefault":
            bg = '#516173'

        case "TamagoDark":
            bg = '#303134'

        case "TamagoLight":
            bg = '#0052e7'

    status1 = 'Enabled' if self.settings['music_playing'] else 'Disabled'
    status2 = 'Enabled' if self.settings['portrait_anim'] else 'Disabled'

    listOfThemes = ['TamagoDefault', 'TamagoDark', 'TamagoLight']

    listOfMusic = ['music1', 'music2', 'music3']

    theme = [
        [sg.Text(f"Current theme: {self.settings['theme']}", background_color=bg, key='_theme_txt_',
            font=('Pokemon Pixel Font', 18, 'normal'))],
        [sg.Combo(listOfThemes, size=(25, 10), default_value=f"{self.settings['theme']}", 
            font=('Pokemon Pixel Font', 20, 'normal'), key='_theme_')],
    ]

    sounds = [
        [sg.Text(f"Current music: {self.settings['music']}", background_color=bg, key='_music_txt_',
            font=('Pokemon Pixel Font', 18, 'normal'))],
        [sg.Combo(listOfMusic, size=(12, 1), default_value=self.settings['music'], key='_music_',
            font=('Pokemon Pixel Font', 20, 'normal')),
        sg.Checkbox(text=status1, default=self.settings['music_playing'], background_color=bg,
            font=('Pokemon Pixel Font', 18, 'normal'), key='_playing_')],
        [sg.Text(f'Music', background_color=bg, font=('Pokemon Pixel Font', 18, 'normal'))],
        [sg.Slider(orientation='h', disable_number_display=True, range=(0, 100), key='_music_vol_',
            default_value=self.settings['music_volume'])],
        [sg.Text(f'Sound', background_color=bg, font=('Pokemon Pixel Font', 18, 'normal'))],
        [sg.Slider(orientation='h', disable_number_display=True, range=(0, 100), key='_sound_vol_',
            default_value=self.settings['sound_volume'])]
    ]

    portrait = [
        [sg.Text('Animated image:', background_color=bg, font=('Pokemon Pixel Font', 18, 'normal')), 
         sg.Checkbox(text=status2, default=self.settings['portrait_anim'], background_color=bg,
            font=('Pokemon Pixel Font', 18, 'normal'), key='_portrait_')]
    ]

    scaling = [
        [sg.Checkbox('0.5x', background_color=bg), sg.Checkbox('1x', background_color=bg), 
         sg.Checkbox('2x', background_color=bg)]
    ]

    elements = [
        [sg.Frame('', theme, s=(210, 65), relief=sg.RELIEF_SUNKEN, background_color=bg,
            pad=((5,5),(5,2)))],
        [sg.Frame('', sounds, s=(210, 190), relief=sg.RELIEF_SUNKEN, background_color=bg,
            pad=((5,5),(2,2)))],
        [sg.Frame('', portrait, s=(210, 35), relief=sg.RELIEF_SUNKEN, background_color=bg,
            pad=((5,5),(2,2)), element_justification='c')],
        [sg.Frame('', scaling, s=(210, 35), relief=sg.RELIEF_SUNKEN, background_color=bg,
            pad=((5,5),(2,0)), element_justification='c')],
        [c.button(self,'Default',0.45), c.button(self,'Apply',0.45), c.button(self,'Back',0.45,
            key='back3')]
    ]

    return elements
