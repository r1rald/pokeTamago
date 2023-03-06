import PySimpleGUI as sg
import src.components as c
import os


def load_poke(self):           
    elements = [
        [sg.Listbox(values=[x for x in self.read_save()], enable_events=True, size=(25, 10),
            key="load")],
        [c.button(self, 'Load', 0.45), c.button(self, 'Delete', 0.45), c.button(self, 'Back', 0.45)]
    ]

    return elements