import PySimpleGUI as sg
import src.components as c
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
        [sg.Listbox(values=[x for x in self.read_save()], s=(1,1), enable_events=True,size=(25, 10),
            key="load")],
        [c.button(self, 'Load', 0.45), c.button(self, 'Delete', 0.45), c.button(self, 'Back', 0.45),
            c.button(self, 'Submit', 0.45, False, False, True)]
    ]

    frame = [
        [sg.Frame('', elements, p=(0,0), element_justification="c", relief=sg.RELIEF_FLAT)]
        ]

    layout = [
        [sg.Frame('', frame, p=(0,0), background_color=titlebar, relief=sg.RELIEF_FLAT)]
    ]

    return layout


def loading_screen(self, player):
    loadScreen = sg.Window('Load', load(self))

    while True:
        event, values = loadScreen.read()  
        loadScreen["load"].bind('<Double-Button-1>', "+-double click-")

        match event:
            case sg.WINDOW_CLOSED | 'BACK':
                break

            case 'LOAD' | 'load+-double click-':
                if not values["load"]:
                    event = c.popUp(self,'','You must choose a save file!',True)

                    if event == 'OK':
                        continue
                else:
                    self.load_saves(player, values["load"][0])
                    player.offline_time()
                    break

            case 'DELETE':
                if not values["load"]:
                    event = c.popUp(self,'','You must choose a save file!',True)

                    if event == 'OK':
                        continue
                else:
                    path = os.path.expanduser('~\\Documents\\pokeTamago\\save')
                    os.remove(f'{path}\\{values["load"][0]}.json')
                    self.read_save()
                    loadScreen['load'].update(values=[x for x in self.read_save()])

    loadScreen.close()