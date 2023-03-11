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

    conditionBar = [
        [sg.Image(f'src\\assets\\img\\types\\none.png', k='type', p=0, size=(30, 24), 
            tooltip=f'', background_color=bg)], [sg.HSeparator(color='#3c4754', p=0)],
        [sg.Image(f'src\\assets\\img\\types\\none.png', k='type2', p=0, size=(30, 24), 
            tooltip=f'', background_color=bg)], [sg.HSeparator(color='#3c4754', p=0)], 
        [sg.HSeparator(color='#3c4754', p=0)]
    ]

    imageLayout = [
        [sg.Graph((170, 100), (0, 100), (170, 0), p=0, key='GRAPH')]
    ]

    elements = [
        [sg.Button('Random', s=(7,1), font=('Poke Pixel Font', 11, 'normal'), border_width=3,
            k='RANDOM', p=((5,0),(5,0))), sg.Input(default_text='--ENTER NAME--',k='-IN-', s=17, 
            justification='c', border_width=3,p=((0,5),(5,0)))],
        [sg.Frame('', imageLayout, size=(168, 100), p=((5,0),(0,0)), element_justification='c',
            border_width=3), sg.Frame('', conditionBar, size=(30, 100), element_justification='c', 
            p=((0,5),(0,0)), background_color=bg, border_width=3)],
        [sg.Input(key='search', s=32, expand_x=False, expand_y=False, justification='c',
            font=('Pokemon Pixel Font', 16, 'normal'), p=((5,5),(0,0)), border_width=2)],
        [sg.Listbox(values=[f'{self.open_dex()[0].index(x)+1}. {x}' for x in self.open_dex()[0]], 
            p=((5,5),(0,10)), enable_events=True, size=(23, 10), key='poke')], 
        [c.button(self,'Choose',0.5,pad=((0,5),(0,5))), c.button(self,'Back',0.5,pad=((5,0),(0,5)),
            key='BACK1')]
    ]

    return elements
