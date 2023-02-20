import PySimpleGUI as sg
from re import sub


def choosePoke(self):
    layout = [
        [sg.Listbox(values=[x for x in self.open_dex()[0]], enable_events=True, size=(25, 15), 
        key="poke", expand_x=True,)],
        [sg.B('Choose', p=((98, 0), (0, 0))), sg.B('Back')]
    ]

    return layout


def choose_pokemon(self, player):
    pokeChooseWin = sg.Window('Choose', choosePoke(self), icon='data\\img\\pokeball.ico')

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
                player.properties['portrait'] = f'data\\img\\poke\\{name}.gif'
                player.properties['type'] = self.open_dex()[1][index]
                player.properties['xp_group'] = self.open_dex()[2][index]
                player.properties['yield'] = self.open_dex()[3][index]
                self.cancel = True
                break

    pokeChooseWin.close()