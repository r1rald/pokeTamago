from nickname_generator import generate
import PySimpleGUI as sg


def newPoke():
    layout = [
        [sg.Text('What is the name of your Pokemon?')],
        [sg.Input(key='-IN-')],
        [sg.B('Random'), sg.Button('Enter', p=((170, 0), (0, 0))), 
        sg.Button('Back'),sg.Button('Submit', visible=False, bind_return_key=True)]
    ]

    return layout


def new_pokemon_screen(self, player):
    pokeName = sg.Window('Name', newPoke(), grab_anywhere=True)

    while True:
        event, values = pokeName.read(timeout=100)

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
                    event, values = sg.Window('error',
                    [[sg.T('Invalid name or this Pokemon is already exist!')],
                    [sg.T('(The name cannot be longer than 14 characters)')],
                    [sg.B('OK', s=(10, 1), p=(10, 10), bind_return_key=True, focus=True)]],
                    keep_on_top=True, auto_close=True, element_justification='c',
                    icon='data\\img\\warning.ico').read(close=True)

    pokeName.close()