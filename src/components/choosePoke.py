import src.components as c
import PySimpleGUI as sg
from re import sub


def choosePoke(self):
    match self.settings['theme']:

        case "TamagoDefault":
            titlebar = '#283b5b'

        case "TamagoDark":
            titlebar = '#303134'

        case "TamagoLight":
            titlebar = '#0052e7'

    elements = [
        [sg.Listbox(values=[x for x in self.open_dex()[0]], enable_events=True, size=(25, 15), 
            key="poke", expand_x=True,)], 
        [c.button(self,'Choose',0.45), c.button(self,'Back',0.45)]
    ]

    frame = [
        [sg.Frame('', elements, p=(0,0), element_justification="c", relief=sg.RELIEF_FLAT)]
        ]

    layout = [
        [sg.Frame('', frame, p=(0,0), background_color=titlebar, relief=sg.RELIEF_FLAT)]
    ]

    return layout


def choose_pokemon(self, player):
    pokeChooseWin = sg.Window('Choose', choosePoke(self))

    while True:
        event, values = pokeChooseWin.read()

        pokeChooseWin["poke"].bind('<Double-Button-1>', "+-double click-")

        match event:
            case sg.WINDOW_CLOSED | 'BACK':
                player.properties['name'] = ""
                break

            case 'CHOOSE' | 'poke+-double click-':
                if values['poke']:
                    index = self.open_dex()[0].index(f'{values["poke"][0]}')
                    name = sub("\s|[']", '', values["poke"][0])
                    player.properties['portrait'] = f'src\\assets\\img\\poke\\{name}.gif'
                    player.properties['type'] = self.open_dex()[1][index]
                    player.properties['xp_group'] = self.open_dex()[2][index]
                    player.properties['yield'] = self.open_dex()[3][index]
                    self.cancel = True
                    break
                else:
                    event = c.popUp(self,'','You must choose a Pokemon!', True)

                    if event == 'OK':
                        continue

    pokeChooseWin.close()