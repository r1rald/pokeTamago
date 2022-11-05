import sys
import funct as f
import subscreens as sc
import layouts as ui
import PySimpleGUI as sg


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
            case 'Options':
                sc.option_screen()

    window1.close()


def mainGame(self):

    mainWindow = sg.Window('pokéTamago', ui.mainGame(self), icon='Data\\img\\logo.ico')

    while True:
        event, value = mainWindow.read(timeout=25)

        match event:
            case sg.WIN_CLOSED | 'Exit':
                self.run = False
                break
            case sg.TIMEOUT_KEY:
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
        mainWindow["image"].UpdateAnimation(
            self.stats['portrait'], time_between_frames=25)

    mainWindow.close()
