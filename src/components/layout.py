import src.hooks.funct as f
import src.components as c
import PySimpleGUI as sg


def newGame(self,player):
    match self.settings['theme']:

        case "TamagoDefault":
            titlebar = '#283b5b'

        case "TamagoDark":
            titlebar = '#303134'

        case "TamagoLight":
            titlebar = '#0052e7'

    elements = [
        [sg.pin(sg.Column(c.main_menu(self), visible=True, element_justification='c', k='menu'))],
        [sg.pin(sg.Column(c.choose_poke(self,player), visible=False, element_justification='c',
            k='choose'))],
        [sg.pin(sg.Column(c.load_poke(self), visible=False, element_justification='c', k='loading'))],
        [sg.pin(sg.Column(c.settings(self), visible=False, element_justification='c', k='settings'))]
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

    elements = [
        [sg.pin(sg.Column(c.main_loop(self, player), visible=True, element_justification='c', 
            k='loop'))],
        [sg.pin(sg.Column(c.death_screen(self, player), visible=False, element_justification='c',
            k='death'))],
        [sg.pin(sg.Column(c.eat_screen(self, player), visible=False, element_justification='c',
            k='eat'))],
        [sg.pin(sg.Column(c.play_screen(self, player), visible=False, element_justification='c',
            k=
            'play'))],
        [sg.pin(sg.Column(c.sleep_screen(self, player), visible=False, element_justification='c',
            k='sleep'))],
        [sg.pin(sg.Column(c.train_screen(self, player), visible=False, element_justification='c',
            k='train'))]
    ]

    frame = [
        [sg.Frame('', elements, p=(0,0), element_justification="c", relief=sg.RELIEF_FLAT)]
        ]

    layout = [
        [sg.Frame('', frame, p=(0,0), background_color=titlebar, relief=sg.RELIEF_FLAT)]
    ]

    return layout
