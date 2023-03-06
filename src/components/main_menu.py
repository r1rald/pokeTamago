import src.components as c
import PySimpleGUI as sg

def main_menu(self):
    buttonColumn = [
        [c.button(self,'New Poke',0.75,False,True,False,(0,2))],
        [c.button(self,'Continue',0.75,False,True,False,(0,2))],
        [c.button(self,'Settings',0.75,False,True,False,(0,2))],
        [c.button(self,'Exit',0.75,False,True,False,(0,2))]
    ]

    elements = [
        [sg.Image('src\\assets\\img\\logo.png', subsample=2, p=(2,2))],
        [sg.Column(buttonColumn)]
    ]

    return elements