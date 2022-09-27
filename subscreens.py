import sys, os, funct as f, PySimpleGUI as sg

def death_screen(self):
    layout1 = [
        [sg.Image('Data\\img\\death.gif',k='image',p=((20,20),(20,0)))],
        [sg.Text('Sadly seems like your pet is passed away.',k='text1',p=((0,0),(20,0)))],
        [sg.Text('Do you want to revive it?',p=((0,0),(0,20)),k='text2')],
        [sg.Button('Revive',size=8,k='r'),sg.Button('Let go',size=8,k='l'),sg.Button('Exit',size=8,p=((50,0),(0,0)))]
    ]
    layout2 = [
        [sg.Image('Data\\img\\revive.gif',k='image',p=((20,20),(20,0)),)],
        [sg.Text('Your pet is about to begin a new life.',k='text1',p=((0,0),(20,0)))],
        [sg.Text(f'The process will take {f.process_time(self.status["revive_time"])}.',p=((0,0),(0,20)),k='text2')],
        [sg.Button('Revive',size=8,k='r'),sg.Button('Let go',size=8,k='l'),sg.Button('Exit',size=8,p=((50,0),(0,0)))]
    ]

    if not self.status["revive"]:
        deathWindow = sg.Window('Passing',layout1,icon='Data\\img\\death.ico',element_justification = "center")
    else:
        deathWindow = sg.Window('Revive',layout2,icon='Data\\img\\death.ico',element_justification = "center")

    while True:
        event, value = deathWindow.read(timeout=150)
        if (event == sg.WIN_CLOSED) or (event == 'Exit'):
            self.run = False
            sys.exit()
        if (event == 'r'):
            self.status['revive'] = True
            self.status['revive_time'] = 604800
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
            deathWindow['image'].UpdateAnimation('Data\\img\\death.gif',time_between_frames=150)
        elif self.status["revive"]:
            deathWindow['image'].UpdateAnimation('Data\\img\\revive.gif',time_between_frames=150)
            deathWindow['text1'].update('Your pet is about to begin a new life.')
            deathWindow['text2'].update(f'The process will take {f.process_time(self.status["revive_time"])}.')
            deathWindow['r'].update(disabled=True)
            deathWindow['l'].update(disabled=True)

    deathWindow.close()


def sleep_screen(self):
    layout = [
        [sg.Image('Data\\img\\sleep.gif',k='image',p=((20,20),(0,0)))],
        [sg.Text('Shhh!!! Your pet is sleeping now.')],
        [sg.Text(f'Let it rest for about {f.process_time(self.status["sleep_time"])}.',p=((0,0),(20,20)),k='text')],
        [sg.Button('Exit',size=8)]
    ]

    sleepWindow = sg.Window('Sleeping',layout,icon='Data\\img\\sleep.ico',element_justification = "center")

    while True:
        event, value = sleepWindow.read(timeout=150)
        if (event == sg.WIN_CLOSED) or (event == 'Exit'):
            self.autosave()
            self.run = False
            sys.exit()
        if self.status['sleeping'] and self.status['sleep_time'] == 0:
            self.status['sleeping'] = False
            break

        sleepWindow['image'].UpdateAnimation('Data\\img\\sleep.gif',time_between_frames=150)
        sleepWindow['text'].update(f'Let it rest for about {f.process_time(self.status["sleep_time"])}.')

    sleepWindow.close()

def eat_screen(self):
    portion = 5

    layout = [
        [sg.Image('Data\\img\\eat.gif',k='image',p=((20,20),(20,20)))],
        [sg.Text(f'You have {portion} portions.',k='text1',p=((0,0),(20,0)))],
        [sg.Text("You don't have any food for now!", visible=False,k='text2')],
        [sg.Text("Your pet is full, you can't feed it for now!", visible=False,k='text3')],
        [sg.Button('Give a snack',size=10,k='snack',p=((0,0),(20,0))),sg.Button('Serve a meal',size=10,k='meal',p=((0,0),(20,0))),sg.Button('Back',size=8,p=((50,0),(20,0)))]
    ]

    eatWindow = sg.Window('Eating',layout,icon='Data\\img\\eat.ico',element_justification = "center")

    while True:
        event, value = eatWindow.read(timeout=150)
        if (event == sg.WIN_CLOSED) or (event == 'Back'):
            break
        if (event == 'snack'):
            portion -= 1
            if self.condition['food'] <= 90 and f.rng(100):
                eatWindow['image'].UpdateAnimation('Data\\img\\snack.gif',time_between_frames=175)
                eatWindow['image'].update('Data\\img\\snack.gif')
                self.condition['food'] += 10
            else:
                eatWindow['image'].update('Data\\img\\eat_miss.gif')
                eatWindow['image'].UpdateAnimation('Data\\img\\eat_miss.gif',time_between_frames=175)
            continue
        if (event == 'meal'):
            portion -= 1
            if self.condition['food'] <= 75 and f.rng(100):
                eatWindow['image'].update('Data\\img\\meal.gif')
                eatWindow['image'].UpdateAnimation('Data\\img\\meal.gif',time_between_frames=175)
                self.condition['food'] += 25
            else:
                eatWindow['image'].update('Data\\img\\eat_miss.gif')
                eatWindow['image'].UpdateAnimation('Data\\img\\eat_miss.gif',time_between_frames=175)
            continue

        eatWindow['image'].UpdateAnimation('Data\\img\\eat.gif',time_between_frames=175)
        eatWindow['text1'].update(f'You have {portion} portions.')

        if portion == 0:
            eatWindow['text2'].update(visible=True)
        if self.condition['food'] > 75:
            eatWindow['meal'].update(disabled=True)
            if self.condition['food'] > 90:
                eatWindow['text3'].update(visible=True)
                eatWindow['snack'].update(disabled=True)

    self.status['eating'] = False
    eatWindow.close()