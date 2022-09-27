import os, sys, funct as f, subscreens as sc, PySimpleGUI as sg


def newGame(self):
    new_game = [[sg.Text("What is your desire?")],
                [sg.Button('Catch new Pokemon'), sg.Button('Continue existing Pokemon'), sg.Button('Exit')]]
    window1 = sg.Window('pokéTamago', new_game, icon='Data\\img\\logo.ico', grab_anywhere=True)

    while True:
        event, values = window1.read()
        if (event == sg.WIN_CLOSED) or (event == 'Exit'):
            sys.exit()
        if (event == 'Catch new Pokemon'):
            f.default_player(self)

            name = [[sg.Text('What is the name of your Pokemon?')],
                    [sg.Input(key='-IN-')],
                    [sg.Button('Enter'), sg.Button('Submit', visible=False, bind_return_key=True)]]
            window2 = sg.Window('Name', name, icon='Data\\img\\logo.ico', grab_anywhere=True)

            while True:
                event, values = window2.read()
                if (event == sg.WINDOW_CLOSED):
                    sys.exit()
                if (event == 'Enter') or (event == 'Submit'):
                    f.saves.clear()
                    f.read_save()
                    if values['-IN-'] in f.saves:
                        sg.Popup('This Pokemon is already exist!',title='error',keep_on_top=True,auto_close=True,auto_close_duration=3,any_key_closes=True,icon='Data\\img\\warning.ico')
                    elif values['-IN-'] == '':
                        sg.Popup('You must give a name to your Pokemon!', title='error',keep_on_top=True,auto_close=True,auto_close_duration=3,any_key_closes=True,icon='Data\\img\\warning.ico')
                    elif len(values['-IN-']) > 14:
                        sg.Popup('Please try a shorter name!',title='error',keep_on_top=True,auto_close=True,auto_close_duration=3,any_key_closes=True,icon='Data\\img\\warning.ico')
                    else:
                        self.stats["name"] = values['-IN-']
                        break

            f.open_dex()

            pokeChoose = [[sg.Listbox(values=[x for x in f.pokes], enable_events=True, size=(25, 15), key="poke", expand_x=True)], 
                    [sg.B('Choose'),sg.Button('Submit', visible=False, bind_return_key=True)]]
            pokeWindow = sg.Window('Load', pokeChoose, icon='Data\\img\\load.ico')

            while True:
                event, values = pokeWindow.read()
                if (event == sg.WINDOW_CLOSED):
                    sys.exit()
                if (event== 'Choose') or (event =='Submit'):
                    index = f.pokes.index(f'{values["poke"][0]}')
                    if ' ' in values["poke"][0]:
                        name = values["poke"][0].replace(' ', '')
                    elif "'" in values["poke"][0]:
                        name = values["poke"][0].replace("'", '')
                    else:
                        name = values["poke"][0]
                    self.stats['portrait'] = f'Data\\img\\poke\\{name}.gif'
                    self.stats['type'] = f.types[index]
                    break

            pokeWindow.close()
            window2.close()

        if (event == 'Continue existing Pokemon'):
            f.saves.clear()
            f.read_save()

            load = [[sg.Listbox(values=[x for x in f.saves], enable_events=True, size=(25, 15), key="load", expand_x=True)], 
            [sg.B('Load'),sg.B('Delete'),sg.Button('Submit', visible=False, bind_return_key=True)]]
            window2 = sg.Window('Load', load, icon='Data\\img\\load.ico')
            
            while True:
                event, values = window2.read()
                if (event == sg.WINDOW_CLOSED):
                    sys.exit()
                if (event == 'Load') or (event == 'Submit'):
                    if not values["load"]:
                        sg.Popup('You must choose a save file!', title='error', keep_on_top=True, auto_close=True, auto_close_duration=3, icon='Data\\img\\warning.ico')
                    else:
                        f.load_saves(self, values["load"][0])
                        break
                if (event == 'Delete'):
                    if not values["load"]:
                        sg.Popup('You must choose a save file!', title='error', keep_on_top=True, auto_close=True, auto_close_duration=3, icon='Data\\img\\warning.ico')
                    else:
                        os.remove(f'Data\\save\\{values["load"][0]}.json')
                        f.saves.clear()
                        f.read_save()
                        window2['load'].update(values=[x for x in f.saves])
            f.offline_time(self)
            window2.close()
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
        if (event == sg.WIN_CLOSED) or (event == 'Exit'):
            self.run = False
            break
        if (event == sg.TIMEOUT_KEY):
            mainWindow.refresh()
        if (event == 'Eat'):
            self.eat()
        if (event == 'Battle'):
            pass
        if (event == 'Training'):
            self.training()
        if (event == 'Play'):
            self.play()
        if (event == 'Sleep'):
            self.sleep()
        if not self.status['alive']:
            sc.death_screen(self)
        if self.status['sleeping']:
            sc.sleep_screen(self)
        if self.status['eating']:
            sc.eat_screen(self)

        if self.condition["exhausted"] < 60:
            xhstdClr = (None)
        elif 80 > self.condition["exhausted"] > 60:
            xhstdClr = ('orange','white')
        else:
            xhstdClr = ('red','white')

        if self.condition["food"] > 50:
            fdClr = (None)
        if self.condition["food"] < 50:
            fdClr = ('green','white')
        if self.condition["food"] < 30:
            fdClr = ('orange','white')
        if self.condition["food"] < 15:
            fdClr = ('red','white')

        if self.condition["bored"] < 60:
            fdClr = (None)
        if self.condition["bored"] > 60:
            fdClr = ('orange','white')
        if self.condition["bored"] > 80:
            fdClr = ('red','white')

        mainWindow['progress_1'].update(self.stats['xp'])
        mainWindow['health'].update(round(self.condition['health']))
        mainWindow['age'].update(f.process_time(self.condition['age']))
        mainWindow['food'].update(self.condition['food'],bar_color=fdClr)
        mainWindow['bored'].update(self.condition['bored'],bar_color=fdClr)
        mainWindow['exhausted'].update(self.condition['exhausted'],bar_color=xhstdClr)  
        mainWindow['Attack'].update(self.stats['Attack'])
        mainWindow['Defense'].update(self.stats['Defense'])
        mainWindow['Sp. Attack'].update(self.stats['Sp. Attack'])
        mainWindow['Sp. Defense'].update(self.stats['Sp. Defense'])
        mainWindow['Speed'].update(self.stats['Speed'])
        mainWindow["image"].UpdateAnimation(self.stats['portrait'],time_between_frames=25)

    mainWindow.close()



