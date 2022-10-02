import os, sys, funct as f, subscreens as sc, PySimpleGUI as sg

def newGame(self):
    buttonColumn = [
        [sg.Button('New Pokemon', size=12)],
        [sg.Button('Load Pokemon', size=12)], 
        [sg.B('Options',size=12)],
        [sg.B('Exit',size=12)]
        ]
    layout = [
        [sg.Image('Data\\img\\logo.png',subsample=3)], 
        [sg.Column(buttonColumn, element_justification='c')]   
        ]

    window1 = sg.Window('', layout, icon='Data\\img\\logo.ico',element_justification='c',grab_anywhere=True)

    while True:
        event, values = window1.read()
        match event:
            case sg.WIN_CLOSED |'Exit':
                sys.exit()
            case 'New Pokemon':
                f.default_player(self)
                sc.new_pokemon_screen(self)
                f.open_dex()
                sc.choose_pokemon(self)
            case 'Load Pokemon':
                f.saves.clear()
                f.read_save()
                sc.loading_screen(self)
        break
    window1.close()


def mainGame(self):
    condition_layout = [
        [sg.T("Health",font=('',10,'bold'),background_color='#506478')],
        [sg.HSeparator(color='#3c4754',p=0)],
        [sg.T("Age",font=('',10,'bold'),background_color='#506478')],
        [sg.HSeparator(color='#3c4754',p=0)],
        [sg.T(f"Food",font=('',10,'bold'),background_color='#506478')],
        [sg.HSeparator(color='#3c4754',p=0)],
        [sg.T(f"Bored",font=('',10,'bold'),background_color='#506478')],
        [sg.HSeparator(color='#3c4754',p=0)],
        [sg.T(f"Exhausted",font=('',10,'bold'),background_color='#506478')]
        ]
    condition_values = [
        [sg.T(f"{round(self.condition['health'])}",font=('',10,'bold'),background_color='#506478',k='health')],
        [sg.HSeparator(color='#3c4754',p=0)],
        [sg.T("",font=('',10,'bold'),background_color='#506478',k='age')],
        [sg.HSeparator(color='#3c4754',p=0)],
        [sg.ProgressBar(max_value=100,orientation='h',expand_x=True,expand_y=True,p=0,key='food',)],
        [sg.HSeparator(color='#3c4754',p=0)],
        [sg.ProgressBar(max_value=100,orientation='h',expand_x=True,expand_y=True,p=0,key='bored',)],
        [sg.HSeparator(color='#3c4754',p=0)],
        [sg.ProgressBar(max_value=100,orientation='h',expand_x=True,expand_y=True,p=0,key='exhausted',)]
        ]
    stats_layout = [
        [sg.T(f"Attack",font=('',10,'bold'),background_color='#506478')],
        [sg.HSeparator(color='#3c4754',p=0)],
        [sg.T(f"Defense",font=('',10,'bold'),background_color='#506478')],
        [sg.HSeparator(color='#3c4754',p=0)],
        [sg.T(f"Sp. Attack",font=('',10,'bold'),background_color='#506478')],
        [sg.HSeparator(color='#3c4754',p=0)],
        [sg.T(f"Sp. Defense",font=('',10,'bold'),background_color='#506478')],
        [sg.HSeparator(color='#3c4754',p=0)],
        [sg.T(f"Speed",font=('',10,'bold'),background_color='#506478')]
        ]
    stats_values = [
        [sg.T(f"{self.stats['Attack']}",font=('',10,'bold'),background_color='#506478',k='Attack')],
        [sg.HSeparator(color='#3c4754',p=0)],
        [sg.T(f"{self.stats['Defense']}",font=('',10,'bold'),background_color='#506478',k='Defense')],
        [sg.HSeparator(color='#3c4754',p=0)],
        [sg.T(f"{self.stats['Sp. Attack']}",font=('',10,'bold'),background_color='#506478',k='Sp. Attack')],
        [sg.HSeparator(color='#3c4754',p=0)],
        [sg.T(f"{self.stats['Sp. Defense']}",font=('',10,'bold'),background_color='#506478',k='Sp. Defense')],
        [sg.HSeparator(color='#3c4754',p=0)],
        [sg.T(f"{self.stats['Speed']}",font=('',10,'bold'),background_color='#506478',k='Speed')]
        ]
    nameLayout = [
        [sg.T(f"{self.stats['name']}".upper(),font=('',15,'bold'),background_color='#506478')],
        [sg.HSeparator(color='#3c4754',p=0)],
        [sg.T(f"Level {self.stats['level']}",font=('',10),background_color='#506478')],
        [sg.ProgressBar(max_value=eval(self.stats['xp_needed']),bar_color=('#28fc03','#525252'),orientation='h',expand_x=True,expand_y=True,relief=sg.RELIEF_RAISED,key='progress_1',)],
        ]
    imageLayout = [
        [sg.Image(self.stats['portrait'],k='image',background_color='#506478',p=0,expand_x=True,expand_y=True)],
        ]

    if len(self.stats["type"]) < 2:
        TypeImage2 = [sg.Image(f'Data\\img\\poke\\types\\none.png',k='type2',background_color='#506478',p=0,size=(30,24),tooltip=' There is no second type of this Pokemon ')]
    else:
        TypeImage2 = [sg.Image(f'Data\\img\\poke\\types\\{self.stats["type"][1]}_Type_Icon.png',k='type2',background_color='#506478',p=0,size=(30,24),tooltip=f' {self.stats["type"][1]} ')]

    conditionBar = [
        [sg.Image(f'Data\\img\\poke\\types\\{self.stats["type"][0]}_Type_Icon.png',k='type1',background_color='#506478',p=0,size=(30,24),tooltip=f' {self.stats["type"][0]} ')],
        [sg.HSeparator(color='#3c4754',p=0)],
        TypeImage2,
        [sg.HSeparator(color='#3c4754',p=0)],
        [sg.HSeparator(color='#3c4754',p=0)]
        ]

    Column = [
        [sg.Frame('',imageLayout,background_color='#506478',size=(170, 100),element_justification='center',p=((0, 0), (0, 5))),sg.Frame('',conditionBar,background_color='#506478',size=(30, 100),element_justification='center',p=((0, 0), (0, 5)))],
        [sg.Frame('',nameLayout,background_color='#506478',size=(200, 90),element_justification='center',p=((0, 0), (5, 5)))],
        [sg.Frame('',condition_layout,background_color='#506478',size=(100,142),element_justification='center',p=((0, 0), (5, 5))), sg.Frame('',condition_values,background_color='#506478',size=(100,142),element_justification='center',p=((0, 0), (5, 5)))],
        [sg.Frame('',stats_layout,background_color='#506478',size=(100,142),element_justification='center',p=((0, 0), (5, 0))), sg.Frame('',stats_values,background_color='#506478',size=(100,142),element_justification='center',p=((0, 0), (5, 0)))]
        ]
    buttonColumn = [
        [sg.B('Eat',size=8)],
        [sg.B('Play',size=8)], 
        [sg.B('Sleep',size=8)],
        [sg.HSeparator(color='#3c4754',p=((0, 0), (10, 10)))],
        [sg.B('Training',size=8)], 
        [sg.B('Battle',size=8)],
        [sg.B('Shop',size=8)],
        [sg.HSeparator(color='#3c4754',p=((0, 0), (10, 10)))],
        [sg.B('Exit',size=8)]
        ]
    layout = [
        [sg.Column(buttonColumn), sg.Column(Column, element_justification='c')],     
        ]
        
    mainWindow = sg.Window('pokéTamago',layout,icon='Data\\img\\logo.ico')

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
            fdClr = ('orange','white')
        else:
            fdClr = ('red','white')

        if self.condition["bored"] < 60:
            brdClr = (None)
        elif 60 < self.condition["bored"] < 80:
            brdClr = ('orange','white')
        else:
            brdClr = ('red','white')

        if self.condition["exhausted"] < 60:
            xhstdClr = (None)
        elif 60 < self.condition["exhausted"] < 80:
            xhstdClr = ('orange','white')
        else:
            xhstdClr = ('red','white')

        mainWindow['progress_1'].update(self.stats['xp'])
        mainWindow['health'].update(round(self.condition['health']))
        mainWindow['age'].update(f.time_counter(self.condition['age']))
        mainWindow['food'].update(self.condition['food'],bar_color=fdClr)
        mainWindow['bored'].update(self.condition['bored'],bar_color=brdClr)
        mainWindow['exhausted'].update(self.condition['exhausted'],bar_color=xhstdClr)  
        mainWindow['Attack'].update(self.stats['Attack'])
        mainWindow['Defense'].update(self.stats['Defense'])
        mainWindow['Sp. Attack'].update(self.stats['Sp. Attack'])
        mainWindow['Sp. Defense'].update(self.stats['Sp. Defense'])
        mainWindow['Speed'].update(self.stats['Speed'])
        mainWindow["image"].UpdateAnimation(self.stats['portrait'],time_between_frames=25)

    mainWindow.close()



