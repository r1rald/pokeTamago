import src.hooks.funct as f
import src.components as c
import PySimpleGUI as sg

def main_menu(self):
    image = [
        [sg.Image(f.image2data(resize=True,path='logo',size=0.4), p=(0,5))],
    ]

    buttons = [
        [c.button(self,'New Poke',0.65,False,True,False,(0,2))],
        [c.button(self,'Continue',0.65,False,True,False,(0,2))],
        [c.button(self,'Settings',0.65,False,True,False,(0,2))],
        [c.button(self,'Exit',0.65,False,True,False,(0,2))]
    ]


    combined = [
        [sg.Column(image, p=((0,0),(50,0)))],
        [sg.Column(buttons, p=0)]
    ]
    
    elements = [
        [sg.Frame('', combined, size=(200, 345), border_width=0, element_justification='c')],
    ]

    return elements