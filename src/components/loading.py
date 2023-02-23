import PySimpleGUI as sg
import os


def load(self):
    match self.settings['theme']:

        case "TamagoDefault":
            titlebar = '#283b5b'

        case "TamagoDark":
            titlebar = '#303134'

        case "TamagoLight":
            titlebar = '#0052e7'
                
    elements = [
        [sg.Listbox(values=[x for x in self.read_save()], enable_events=True, key="load")],
        [sg.B('Load', p=((55, 0), (0, 0))), sg.B('Delete'), sg.B('Back'), 
        sg.B('Submit', visible=False, bind_return_key=True)]
    ]

    frame = [
        [sg.Frame('', elements, p=(0,0), element_justification="c", relief=sg.RELIEF_FLAT)]
        ]

    layout = [
        [sg.Frame('', frame, p=(0,0), background_color=titlebar, relief=sg.RELIEF_FLAT)]
    ]

    return layout


def loading_screen(self, player):
    loadScreen = sg.Window('Load', load(self), icon='data\\img\\load.ico')

    while True:
        event, values = loadScreen.read()  
        loadScreen["load"].bind('<Double-Button-1>', "+-double click-")

        match event:
            case sg.WINDOW_CLOSED | 'Back':
                break

            case 'Load' | 'load+-double click-':
                if not values["load"]:
                    sg.Popup('You must choose a save file!', title='error', keep_on_top=True,
                    auto_close=True, icon='data\\img\\warning.ico')
                else:
                    self.load_saves(player, values["load"][0])
                    player.offline_time()
                    break

            case 'Delete':
                if not values["load"]:
                    sg.Popup('You must choose a save file!', title='error', keep_on_top=True,
                    auto_close=True, icon='data\\img\\warning.ico')
                else:
                    path = os.path.expanduser('~\\Documents\\pokeTamago\\save')
                    os.remove(f'{path}\\{values["load"][0]}.json')
                    self.read_save()
                    loadScreen['load'].update(values=[x for x in self.read_save()])

    loadScreen.close()