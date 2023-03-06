import PySimpleGUI as sg
import src.components as c


def pop_up_layout(self, message):
    match self.settings['theme']:

        case "TamagoDefault":
            titlebar = '#283b5b'

        case "TamagoDark":
            titlebar = '#303134'

        case "TamagoLight":
            titlebar = '#0052e7'

    elements = [
        [sg.T(message, justification='c')], 
        [c.button(self,'Ok',0.5,pad=(5,5)), c.button(self,'Cancel',0.5,pad=(5,5))]
        ]

    frame = [
        [sg.Frame('', elements, p=(0,0), element_justification="c", relief=sg.RELIEF_FLAT)]
        ]

    layout = [
        [sg.Frame('', frame, p=(0,0), background_color=titlebar, relief=sg.RELIEF_FLAT)]
    ]

    return layout
                    

def pop_up(self,name,message,button=None):
    popUp = sg.Window(name, pop_up_layout(self,message), keep_on_top=True, 
        enable_close_attempted_event=True, disable_minimize=True)
    
    while True:
        event, values = popUp.read(timeout=24)
        
        match event:

            case 'OK':
                break

            case 'CANCEL' | sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
                break

        if button:
            popUp['CANCEL'].update(visible=False)

    popUp.close()
    return event



