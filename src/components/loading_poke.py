import PySimpleGUI as sg
import src.components as c
import os


def load_poke(self):
    match self.settings['theme']:

        case "TamagoDefault":
            bg = '#516173'

        case "TamagoDark":
            bg = '#303134'

        case "TamagoLight":
            bg = '#0052e7'

    imageLayout = [
        [sg.Graph((170, 100), (0, 100), (170, 0), p=0, key='GRAPH2')]
    ]

    conditionBar = [
        [sg.Image(None, p=1, k='type3', background_color=bg, tooltip='')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.Image(None, p=1, k='type4', background_color=bg, tooltip='')],
        [sg.HSeparator(color='#3c4754', p=0)], 
        [sg.Image(None, p=1, k='mood', background_color=bg, tooltip='')], 
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.Image(None, p=1, k='xy', background_color=bg, tooltip='')],
    ]


    statusLayout = [
        [sg.Text('LEVEL 0', font=('Pokemon Pixel Font', 18, 'bold'), background_color=bg,
            justification='c', k='head1'), sg.VSeparator(color='#3c4754', p=0),
         sg.Text('NONE', font=('Pokemon Pixel Font', 18, 'bold'), background_color=bg,
            justification='c', k='head2'), sg.VSeparator(color='#3c4754', p=0),
         sg.Text('NONE', font=('Pokemon Pixel Font', 18, 'bold'), background_color=bg,
            justification='c', k='head3')]
    ]

    listbox = [
        [sg.Listbox(values=[x for x in self.read_save()], enable_events=True, size=(23, 11), p=0,
            key="load")]
    ]

    combined = [
        [sg.Column(statusLayout, p=0, background_color=bg, justification='c')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.Column(imageLayout, p=0, background_color=bg), sg.VSeparator(color='#3c4754', p=0), 
         sg.Column(conditionBar, p=0, background_color=bg, element_justification='c')],
        [sg.Column(listbox, p=0)]
    ]

    elements = [
        [sg.Frame('', combined, size=(200, 345), p=5, border_width=3, background_color=bg)],
        [c.button(self, 'Load', 0.45), c.button(self, 'Delete', 0.45), c.button(self, 'Back', 0.45,
            key='back2')]
    ]

    return elements
