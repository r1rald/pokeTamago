import sys
import os
import funct as f
import subscreens as sc
import layouts as ui
import PySimpleGUI as sg
from PIL import Image
from threading import Thread
from time import sleep


def newGame(self):
    window1 = sg.Window('', ui.newGame(), icon='Data\\img\\logo.ico',
                        element_justification='c', grab_anywhere=True)

    while True:
        event, values = window1.read()
        match event:
            case sg.WIN_CLOSED | 'Exit':
                sys.exit()
            case 'New Pokemon':
                f.default_player(self)
                sc.new_pokemon_screen(self)
                if self.stats['name']:
                    f.open_dex()
                    sc.choose_pokemon(self)
                    if self.stats['portrait']:
                        break
                else:
                    continue
            case 'Continue':
                f.load_saves.has_been_called = False
                f.saves.clear()
                f.read_save()
                sc.loading_screen(self)
                if f.load_saves.has_been_called:
                    break
                else:
                    continue
            case 'Settings':
                sc.settings_screen(self)

    window1.close()


def mainGame(self):
    global index, frames, size

    def portrait_thread():
        global index
        while True:
            sleep(0.03)
            index = (index + 1) % frames
            if not self.run:
                break

    im = Image.open(self.stats['portrait'])
    width, height = im.size
    frames = im.n_frames

    graph_width, graph_height = size = (170, 100)

    mainWindow = sg.Window('pokéTamago', ui.mainGame(
        self), icon='Data\\img\\logo.ico', finalize=True)

    mainWindow['GRAPH'].draw_image(
        f'{f.portrait_background(self)}', location=(0, 0))

    index = 0 if self.settings['portrait_anim'] else 10
    im.seek(index)
    x, y = location = (graph_width//2-width//2, graph_height//2-height//2)
    item = mainWindow['GRAPH'].draw_image(
        data=f.image_to_data(im), location=location)

    thread = Thread(target=portrait_thread, daemon=True)
    if self.settings['portrait_anim']:
        thread.start()

    while True:
        event, value = mainWindow.read(timeout=25)
        match event:
            case sg.WIN_CLOSED | 'Exit':
                self.run = False
                break
            case sg.TIMEOUT_KEY:
                im.seek(index)
                item_new = mainWindow['GRAPH'].draw_image(
                    data=f.image_to_data(im), location=location)
                mainWindow['GRAPH'].delete_figure(item)
                item = item_new
                mainWindow.refresh()
            case 'Eat':
                self.eat()
            case 'Battle':
                pass
            case 'Training':
                self.training()
            case 'Play':
                self.play()
            case 'Sleep':
                self.sleep()
            case 'Main Menu':
                self.run = False
                os.execl(sys.executable, sys.executable, *sys.argv)

        if not self.status['alive']:
            sc.death_screen(self)
        if self.status['sleeping']:
            sc.sleep_screen(self)
        if self.status['eating']:
            sc.eat_screen(self)

        if 40 < self.condition["food"]:
            fdClr = (None)
        elif 20 < self.condition["food"] < 40:
            fdClr = ('orange', 'white')
        else:
            fdClr = ('red', 'white')

        if self.condition["bored"] < 60:
            brdClr = (None)
        elif 60 < self.condition["bored"] < 80:
            brdClr = ('orange', 'white')
        else:
            brdClr = ('red', 'white')

        if self.condition["exhausted"] < 60:
            xhstdClr = (None)
        elif 60 < self.condition["exhausted"] < 80:
            xhstdClr = ('orange', 'white')
        else:
            xhstdClr = ('red', 'white')

        mainWindow['progress_1'].update(self.stats['xp'])
        mainWindow['health'].update(round(self.condition['health']))
        mainWindow['age'].update(f.time_counter(self.condition['age']))
        mainWindow['food'].update(self.condition['food'], bar_color=fdClr)
        mainWindow['bored'].update(self.condition['bored'], bar_color=brdClr)
        mainWindow['exhausted'].update(
            self.condition['exhausted'], bar_color=xhstdClr)
        mainWindow['Attack'].update(self.stats['Attack'])
        mainWindow['Defense'].update(self.stats['Defense'])
        mainWindow['Sp. Attack'].update(self.stats['Sp. Attack'])
        mainWindow['Sp. Defense'].update(self.stats['Sp. Defense'])
        mainWindow['Speed'].update(self.stats['Speed'])

    mainWindow.close()
