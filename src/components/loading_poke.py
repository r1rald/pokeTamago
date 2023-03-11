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

    conditionBar = [
        [sg.Image(f'src\\assets\\img\\types\\none.png', k='type3', p=0, size=(30, 24), 
            tooltip=f'', background_color=bg)], [sg.HSeparator(color='#3c4754', p=0)],
        [sg.Image(f'src\\assets\\img\\types\\none.png', k='type4', p=0, size=(30, 24), 
            tooltip=f'', background_color=bg)], [sg.HSeparator(color='#3c4754', p=0)], 
        [sg.HSeparator(color='#3c4754', p=0)]
    ]

    imageLayout = [
        [sg.Graph((170, 100), (0, 100), (170, 0), p=0, key='GRAPH2')]
    ]

    nameLayout = [
        [sg.Text('', font=('Pokemon Pixel Font', 18, 'bold'), background_color=bg,
            justification='c', k='head1'), sg.VSeparator(color=bg, p=0, k='0101'),
         sg.Text('', font=('Pokemon Pixel Font', 18, 'bold'), background_color=bg,
            justification='c', k='head2'), sg.VSeparator(color=bg, p=0, k='0202'),
         sg.Text('', font=('Pokemon Pixel Font', 18, 'bold'), background_color=bg,
            justification='c', k='head3')]
    ]

    elements = [
        [sg.Frame('', nameLayout,  p=((5,5),(5,0)), border_width=3, element_justification='c',
            size=(198,30), background_color=bg)],
        [sg.Frame('', imageLayout, size=(168, 100), p=((5,0),(0,0)), element_justification='c',
            border_width=3), sg.Frame('', conditionBar, size=(30, 100), element_justification='c', 
            p=((0,5),(0,0)), background_color=bg, border_width=3)],
        [sg.Listbox(values=[x for x in self.read_save()], enable_events=True, size=(23, 11),
            p=((5,5),(0,0)), key="load")],
        [c.button(self, 'Load', 0.45), c.button(self, 'Delete', 0.45), c.button(self, 'Back', 0.45,
            key='back2')]
    ]

    return elements
