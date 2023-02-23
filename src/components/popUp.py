import PySimpleGUI as sg


def popUp_layout(self, message):
    match self.settings['theme']:

        case "TamagoDefault":
            titlebar = '#283b5b'

        case "TamagoDark":
            titlebar = '#303134'

        case "TamagoLight":
            titlebar = '#0052e7'

    elements = [
        [sg.T(message, justification='c')], [sg.Button('OK'), sg.B('Cancel', k='c')]
        ]

    frame = [
        [sg.Frame('', elements, p=(0,0), element_justification="c", relief=sg.RELIEF_FLAT)]
        ]

    layout = [
        [sg.Frame('', frame, p=(0,0), background_color=titlebar, relief=sg.RELIEF_FLAT)]
    ]

    return layout
                    

def popUp(self,name,message,button=None):
    popUp = sg.Window(name, popUp_layout(self,message), icon='data\\img\\warning.ico',
        keep_on_top=True, enable_close_attempted_event=True, disable_minimize=True)
    
    while True:
        event, values = popUp.read(timeout=1)
        
        match event:

            case 'OK':
                break

            case 'c' | sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
                break

        if button:
            popUp['c'].update(visible=False)

    popUp.close()
    return event



