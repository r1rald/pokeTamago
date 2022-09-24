import os, sys, time, funct as f, PySimpleGUI as sg


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
                        sg.Popup('This Pokemon is already exist!', title='error', keep_on_top=True, auto_close=True, auto_close_duration=3, icon='Data\\img\\warning.ico')
                    elif values['-IN-'] == '':
                        sg.Popup('You must give a name to your Pokemon!', title='error', keep_on_top=True, auto_close=True, auto_close_duration=3, icon='Data\\img\\warning.ico')
                    elif len(values['-IN-']) > 14:
                        sg.Popup('Please try a shorter name!', title='error', keep_on_top=True, auto_close=True, auto_close_duration=3, icon='Data\\img\\warning.ico')
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
        event,value = mainWindow.read(timeout=25)
        if (event == sg.WIN_CLOSED) or (event == 'Exit'):
            self.autosave()
            self.run = False
            break
        if event == sg.TIMEOUT_KEY:
            mainWindow.refresh()
        if event == 'Eat':
            self.eat()
        if event == 'Battle':
            pass
        if event == 'Training':
            self.training()
        if event == 'Play':
            self.play()
        if event == 'Sleep':
            self.sleep()
        if not self.status['alive']:
            death_screen(self)

        if self.condition["exhausted"] < 60:
            xhstdClr = (None)
        if self.condition["exhausted"] > 60:
            xhstdClr = ('orange','white')
        if self.condition["exhausted"] > 80:
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


def death_screen(self):
    layout1 = [
        [sg.Image(f'Data\\img\\death.gif',k='image',p=((20,20),(20,0)))],
        [sg.Text('''Sadly seems like your pet is passed away.
    Do you want to revive this Pokemon?''',p=((0,0),(20,20)),k='text')],
        [sg.Button('Revive',size=8,k='r'),sg.Button('Let go',size=8,k='l'),sg.Button('Exit',size=8,p=((50,0),(0,0)))]
    ]
    layout2 = [
        [sg.Image(f'Data\\img\\revive.gif',k='image',p=((20,20),(20,0)),)],
        [sg.Text(f'''Your Pokemon is about to begin a new life.
    The process will take {f.process_time(self.status["revive_time"])}.''',p=((0,0),(20,20)),k='text')],
        [sg.Button('Revive',size=8,k='r'),sg.Button('Let go',size=8,k='l'),sg.Button('Exit',size=8,p=((50,0),(0,0)))]
    ]

    if not self.status["revive"]:
        deathWindow = sg.Window('Passing',layout1,icon='Data\\img\\death.ico',element_justification = "center")
    else:
        deathWindow = sg.Window('Revive',layout2,icon='Data\\img\\death.ico',element_justification = "center")

    while True:
        event,value = deathWindow.read(timeout=150)
        if (event == sg.WIN_CLOSED) or (event == 'Exit'):
            self.autosave()
            self.run = False
            sys.exit()
        if (event == 'r'):
            self.status['revive'] = True
            self.status['revive_time'] = 60
        if (event == 'l'):
            os.remove(f'Data\\save\\{self.stats["name"]}.json')
            self.run = False
            sys.exit()
        if self.status['revive'] and self.status['revive_time'] == 0:
            self.condition['health'] = self.stats['MaxHP']
            self.condition['bored'] = 0
            self.condition['food'] = 100
            self.condition['exhausted'] = 0
            self.status['alive'] = True
            self.status['revive'] = False
            break

        if not self.status["revive"]:
            deathWindow['image'].UpdateAnimation(f'Data\\img\\death.gif',time_between_frames=150)
        elif self.status["revive"]:
            deathWindow['image'].UpdateAnimation(f'Data\\img\\revive.gif',time_between_frames=150)
            deathWindow['text'].update(f'''Your Pokemon is about to begin a new life.
    The process will take {f.process_time(self.status["revive_time"])}.''')
            deathWindow['r'].update(disabled=True)
            deathWindow['l'].update(disabled=True)

    deathWindow.close()