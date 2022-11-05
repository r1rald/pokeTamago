from random import randint
import funct as f
import PySimpleGUI as sg


def newGame():

    buttonColumn = [
        [sg.Button('New Pokemon', size=12)],
        [sg.Button('Continue', size=12)],
        [sg.B('Options', size=12)],
        [sg.B('Exit', size=12)]
    ]
    layout = [
        [sg.Image('Data\\img\\logo.png', subsample=3)],
        [sg.Column(buttonColumn, element_justification='c')]
    ]

    return layout


def mainGame(self):

    condition_layout = [
        [sg.T("Health", font=('', 10, 'bold'), background_color='#242124')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T("Age", font=('', 10, 'bold'), background_color='#242124')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Food", font=('', 10, 'bold'), background_color='#242124')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Bored", font=('', 10, 'bold'), background_color='#242124')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Exhausted", font=('', 10, 'bold'), background_color='#242124')]
    ]
    condition_values = [
        [sg.T(f"{round(self.condition['health'])}", font=(
            '', 10, 'bold'), background_color='#242124', k='health')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T("", font=('', 10, 'bold'), background_color='#242124', k='age')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.ProgressBar(max_value=100, orientation='h',
                        expand_x=True, expand_y=True, p=0, key='food',)],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.ProgressBar(max_value=100, orientation='h',
                        expand_x=True, expand_y=True, p=0, key='bored',)],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.ProgressBar(max_value=100, orientation='h',
                        expand_x=True, expand_y=True, p=0, key='exhausted',)]
    ]
    stats_layout = [
        [sg.T(f"Attack", font=('', 10, 'bold'), background_color='#242124')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Defense", font=('', 10, 'bold'), background_color='#242124')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Sp. Attack", font=('', 10, 'bold'), background_color='#242124')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Sp. Defense", font=('', 10, 'bold'), background_color='#242124')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Speed", font=('', 10, 'bold'), background_color='#242124')]
    ]
    stats_values = [
        [sg.T(f"{self.stats['Attack']}", font=('', 10, 'bold'),
              background_color='#242124', k='Attack')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{self.stats['Defense']}", font=('', 10, 'bold'),
              background_color='#242124', k='Defense')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{self.stats['Sp. Attack']}", font=('', 10, 'bold'),
              background_color='#242124', k='Sp. Attack')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{self.stats['Sp. Defense']}", font=('', 10, 'bold'),
              background_color='#242124', k='Sp. Defense')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{self.stats['Speed']}", font=('', 10, 'bold'),
              background_color='#242124', k='Speed')]
    ]
    nameLayout = [
        [sg.T(f"{self.stats['name']}".upper(), font=(
            '', 15, 'bold'), background_color='#242124')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Level {self.stats['level']}", font=(
            '', 10), background_color='#242124')],
        [sg.ProgressBar(max_value=eval(self.stats['xp_needed']), bar_color=('#28fc03', '#525252'),
                        orientation='h', expand_x=True, expand_y=True, relief=sg.RELIEF_RAISED, key='progress_1',)],
    ]
    imageLayout = [
        [sg.Image(self.stats['portrait'], k='image',
                  background_color='#242124', p=0, expand_x=True, expand_y=True)],
    ]

    if len(self.stats["type"]) < 2:
        TypeImage2 = [sg.Image(f'Data\\img\\poke\\types\\none.png', k='type2', background_color='#242124', p=0, size=(
            30, 24), tooltip=' There is no second type of this Pokemon ')]
    else:
        TypeImage2 = [sg.Image(f'Data\\img\\poke\\types\\{self.stats["type"][1]}_Type_Icon.png', k='type2',
                               background_color='#242124', p=0, size=(30, 24), tooltip=f' {self.stats["type"][1]} ')]

    conditionBar = [
        [sg.Image(f'Data\\img\\poke\\types\\{self.stats["type"][0]}_Type_Icon.png', k='type1',
                  background_color='#242124', p=0, size=(30, 24), tooltip=f' {self.stats["type"][0]} ')],
        [sg.HSeparator(color='#3c4754', p=0)],
        TypeImage2,
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.HSeparator(color='#3c4754', p=0)]
    ]

    Column = [
        [sg.Frame('', imageLayout, background_color='#242124', size=(170, 100), element_justification='center', p=((0, 0), (0, 5))), sg.Frame(
            '', conditionBar, background_color='#242124', size=(30, 100), element_justification='center', p=((0, 0), (0, 5)))],
        [sg.Frame('', nameLayout, background_color='#242124', size=(
            200, 90), element_justification='center', p=((0, 0), (5, 5)))],
        [sg.Frame('', condition_layout, background_color='#242124', size=(100, 142), element_justification='center', p=((0, 0), (5, 5))), sg.Frame(
            '', condition_values, background_color='#242124', size=(100, 142), element_justification='center', p=((0, 0), (5, 5)))],
        [sg.Frame('', stats_layout, background_color='#242124', size=(100, 142), element_justification='center', p=((0, 0), (5, 0))), sg.Frame(
            '', stats_values, background_color='#242124', size=(100, 142), element_justification='center', p=((0, 0), (5, 0)))]
    ]
    buttonColumn = [
        [sg.B('Eat', size=8)],
        [sg.B('Play', size=8)],
        [sg.B('Sleep', size=8)],
        [sg.HSeparator(color='#3c4754', p=((0, 0), (10, 10)))],
        [sg.B('Training', size=8)],
        [sg.B('Battle', size=8)],
        [sg.B('Shop', size=8)],
        [sg.HSeparator(color='#3c4754', p=((0, 0), (10, 10)))],
        [sg.B('Exit', size=8)]
    ]
    layout = [
        [sg.Column(buttonColumn), sg.Column(
            Column, element_justification='c')],
    ]

    return layout


def newPoke():

    layout = [
        [sg.Text('What is the name of your Pokemon?')],
        [sg.Input(key='-IN-')],
        [sg.Button('Enter', p=((238, 0), (0, 0))), sg.Button('Back'),
         sg.Button('Submit', visible=False, bind_return_key=True)]
    ]

    return layout


def choosePoke():

    layout = [
        [sg.Listbox(values=[x for x in f.pokes], enable_events=True,
                    size=(25, 15), key="poke", expand_x=True)],
        [sg.B('Choose', p=((98, 0), (0, 0))), sg.B('Back'), sg.Button(
            'Submit', visible=False, bind_return_key=True)]
    ]

    return layout


def load():

    layout = [
        [sg.Listbox(values=[x for x in f.saves], enable_events=True,
                    size=(25, 15), key="load", expand_x=True)],
        [sg.B('Load', p=((58, 0), (0, 0))), sg.B('Delete'), sg.B('Back'),
         sg.B('Submit', visible=False, bind_return_key=True)]
    ]

    return layout


def options():

    listOfThemes = ['TamagoDefault', 'TamagoDark', 'TamagoLight']
    listOfMusic = ['asd']

    theme = [
        [sg.T(f'Current theme: ', key='theme_txt')],
        [sg.Combo(listOfThemes, size=(25, 10),
                  default_value='BrownBlue', key='theme')],
    ]
    sounds = [
        [sg.T(f'Current music: ')],
        [sg.Combo(listOfMusic, size=(14, 0), default_value='asd',
                  key='music_txt'), sg.Checkbox('Enable', default=True)],
        [sg.T(f'Overall')],
        [sg.Slider(orientation='h', disable_number_display=True,
                   range=(0, 100), default_value=100)],
        [sg.T(f'Music')],
        [sg.Slider(orientation='h', disable_number_display=True,
                   range=(0, 100), default_value=100)],
        [sg.T(f'Effects')],
        [sg.Slider(orientation='h', disable_number_display=True,
                   range=(0, 100), default_value=100)]
    ]
    layout = [
        [sg.Frame('Theme', theme)],
        [sg.Frame('Audio', sounds)],
        [sg.B('Apply', p=((123, 0), (0, 0))), sg.B('Back')]
    ]

    return layout


def dead1():

    layout = [
        [sg.Image('Data\\img\\death.gif', k='image', p=((20, 20), (20, 0)))],
        [sg.Text('Sadly seems like your pet is passed away.',
                 k='text1', p=((0, 0), (20, 0)))],
        [sg.Text('Do you want to revive it?', p=((0, 0), (0, 20)), k='text2')],
        [sg.Button('Revive', size=8, k='r'), sg.Button(
            'Let go', size=8, k='l'), sg.Button('Exit', size=8, p=((50, 0), (0, 0)))]
    ]
    
    return layout


def dead2(self):

    layout = [
        [sg.Image('Data\\img\\revive.gif', k='image', p=((20, 20), (20, 0)),)],
        [sg.Text('Your pet is about to begin a new life.',
                 k='text1', p=((0, 0), (20, 0)))],
        [sg.Text(f'The process will take {f.time_counter(self.status["revive_time"])}.', p=(
            (0, 0), (0, 20)), k='text2')],
        [sg.Button('Revive', size=8, k='r'), sg.Button(
            'Let go', size=8, k='l'), sg.Button('Exit', size=8, p=((50, 0), (0, 0)))]
    ]
    
    return layout


def sleeping(self):

    layout = [
        [sg.Image('Data\\img\\sleep.gif', k='image', p=((20, 20), (0, 0)))],
        [sg.Text('Shhh!!! Your pet is sleeping now.')],
        [sg.Text(f'Let it rest for about {f.time_counter(self.status["sleep_time"])}.', p=(
            (0, 0), (20, 20)), k='text')],
        [sg.Button('Exit', size=8)]
    ]

    return layout


def eating():

    portion = randint(5, 10)

    layout = [
        [sg.Image('Data\\img\\eat.gif', k='image', p=((20, 20), (20, 20)))],
        [sg.Text(f'You have {portion} portions.',
                 k='text1', p=((0, 0), (20, 0)))],
        [sg.Text("You don't have any food for now!", visible=False, k='text2')],
        [sg.Text("Your pet is full, you can't feed it for now!",
                 visible=False, k='text3')],
        [sg.Button('Give a snack', size=10, k='snack', p=((0, 0), (20, 0))), sg.Button(
            'Serve a meal', size=10, k='meal', p=((0, 0), (20, 0))), sg.Button('Back', size=8, p=((50, 0), (20, 0)))]
    ]

    return layout

