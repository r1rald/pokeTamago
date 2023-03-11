import src.components as c
import PySimpleGUI as sg


def choose_poke(self,player):
    match self.settings['theme']:

        case "TamagoDefault":
            bg = '#516173'

        case "TamagoDark":
            bg = '#303134'

        case "TamagoLight":
            bg = '#0052e7'

    nameLayout = [
        [sg.Button('Random', s=(7,1), font=('Poke Pixel Font', 11, 'normal'), k='RANDOM', p=0), 
         sg.Input(default_text='--ENTER NAME--',k='-IN-', s=18, justification='c', p=0)],
    ]

    imageLayout = [
        [sg.Graph((170, 100), (0, 100), (170, 0), p=0, key='GRAPH'), 
         sg.VSeparator(color='#3c4754', p=0)],
    ]

    conditionBar = [
        [sg.Image(None, p=1, k='type1', background_color=bg, tooltip='')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.Image(None, p=1, k='type2', background_color=bg, tooltip='')],
        [sg.HSeparator(color='#3c4754', p=0)], 
        [sg.Image(None, p=1, k='group', background_color=bg, tooltip='')], 
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.Image(None, p=1, k='nature', background_color=bg, tooltip='')],
    ]

    searchBar = [
        [sg.Input(key='search', s=32, justification='c', font=('Pokemon Pixel Font', 16, 'normal'), 
            p=0)],
        [sg.Listbox(values=[f'{self.open_dex()[0].index(x)+1}. {x}' for x in self.open_dex()[0]], 
            p=0, enable_events=True, size=(23, 10), key='poke')]
    ]

    combined = [
        [sg.Column(nameLayout, p=0)],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.Column(imageLayout, p=0, background_color=bg), 
         sg.Column(conditionBar, p=0, background_color=bg, element_justification='c')],
        [sg.Column(searchBar, p=0)]
    ]

    elements = [
        [sg.Frame('', combined, size=(200, 345), p=5, border_width=3, background_color=bg)],
        [c.button(self,'Choose',0.5,pad=((0,5),(0,5))), 
         c.button(self,'Back',0.5,pad=((5,0),(0,5)), key='BACK1')]
    ]

    return elements
