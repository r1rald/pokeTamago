from nickname_generator import generate
import src.components as c
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
        [c.button(self,'Random',0.45), c.button(self,'Enter',0.45), c.button(self,'Back',0.45),
         c.button(self,'Submit',0.45,False,False,True)]
    ]

    frame = [
        [sg.Frame('', elements, p=(0,0), element_justification="c", relief=sg.RELIEF_FLAT)]
        ]

    layout = [
        [sg.Frame('', frame, p=(0,0), background_color=titlebar, relief=sg.RELIEF_FLAT)]
    ]

    return layout


def new_pokemon_screen(self, player):
    pokeName = sg.Window('Name', newPoke(self), enable_close_attempted_event=True)

    while True:
        event, values = pokeName.read(timeout=24)

        match event:
            case sg.TIMEOUT_KEY:
                pokeName.refresh()

            case sg.WINDOW_CLOSE_ATTEMPTED_EVENT | 'BACK':
                event = c.popUp(self,'','Are you sure you want to continue?')

                if event == 'OK':
                    self.cancel = True
                    break

                if event == 'CANCEL':
                    continue
            
            case 'RANDOM':
                pokeName['-IN-'].update(value=generate())

            case 'ENTER' | 'SUBMIT':
                if 1 <= len(values['-IN-']) <= 14 and values['-IN-'] not in self.read_save():
                    player.properties["name"] = values['-IN-']
                    break
                else:
                    c.popUp(self, '', 'Invalid name or this Pokemon is already exist!\n'+
                    '(The name cannot be longer than 14 characters)', True)

    pokeName.close()