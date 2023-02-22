from nickname_generator import generate
import Data.screens as sc
import PySimpleGUI as sg


def newPoke(self):
    match self.settings['theme']:

        case "TamagoDefault":
            titlebar = '#283b5b'

        case "TamagoDark":
            titlebar = '#303134'

        case "TamagoLight":
            titlebar = '#0052e7'

    elements = [
        [sg.Text('What is the name of your Pokemon?')],
        [sg.Input(key='-IN-', s=48, expand_x=False, expand_y=False, justification='l')],
        [sg.B('Random'), sg.Button('Enter', p=((170, 0), (0, 0))), 
        sg.Button('Back'),sg.Button('Submit', visible=False, bind_return_key=True)]
    ]

    frame = [
        [sg.Frame('', elements, p=(0,0), element_justification="c", relief=sg.RELIEF_FLAT)]
        ]

    layout = [
        [sg.Frame('', frame, p=(0,0), background_color=titlebar, relief=sg.RELIEF_FLAT)]
    ]

    return layout


def new_pokemon_screen(self, player):
    pokeName = sg.Window('Name', newPoke(self), grab_anywhere=True)

    while True:
        event, values = pokeName.read(timeout=41.66)

        match event:
            case sg.TIMEOUT_KEY:
                pokeName.refresh()

            case sg.WINDOW_CLOSED | 'Back':
                self.cancel = True
                break
            
            case 'Random':
                pokeName['-IN-'].update(value=generate())

            case 'Enter' | 'Submit':
                if 1 <= len(values['-IN-']) <= 14 and values['-IN-'] not in self.read_save():
                    player.properties["name"] = values['-IN-']
                    break
                else:
                    sc.popUp(self, 'error', 'Invalid name or this Pokemon is already exist!\n'+
                    '(The name cannot be longer than 14 characters)', True)

    pokeName.close()