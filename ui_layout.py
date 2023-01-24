from random import randint
import funct as f
import PySimpleGUI as sg


def newGame():
    buttonColumn = [
        [sg.Button('New Pokemon', size=12)],
        [sg.Button('Continue', size=12)],
        [sg.B('Settings', size=12)],
        [sg.B('Exit', size=12)]
    ]
    layout = [
        [sg.Image('Data\\img\\logo.png', subsample=3)],
        [sg.Column(buttonColumn, element_justification='c')]
    ]

    return layout


def mainGame(self, player):
    condition_layout = [
        [sg.T("Health", font=('', 10, 'bold'),
              background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T("Age", font=('', 10, 'bold'),
              background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Food", font=('', 10, 'bold'),
              background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Bored", font=('', 10, 'bold'),
              background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Exhausted", font=('', 10, 'bold'),
              background_color=self.settings['background'])]
    ]
    condition_values = [
        [sg.T(f"{round(player.condition['health'])}", font=(
            '', 10, 'bold'), k='health', background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T("", font=('', 10, 'bold'), k='age',
              background_color=self.settings['background'])],
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
        [sg.T(f"Attack", font=('', 10, 'bold'),
              background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Defense", font=('', 10, 'bold'),
              background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Sp. Attack", font=('', 10, 'bold'),
              background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Sp. Defense", font=('', 10, 'bold'),
              background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Speed", font=('', 10, 'bold'),
              background_color=self.settings['background'])]
    ]
    stats_values = [
        [sg.T(f"{player.stats['Attack']}", font=('', 10, 'bold'),
              background_color=self.settings['background'], k='Attack')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{player.stats['Defense']}", font=('', 10, 'bold'),
              background_color=self.settings['background'], k='Defense')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{player.stats['Sp. Attack']}", font=('', 10, 'bold'),
              background_color=self.settings['background'], k='Sp. Attack')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{player.stats['Sp. Defense']}", font=('', 10, 'bold'),
              background_color=self.settings['background'], k='Sp. Defense')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{player.stats['Speed']}", font=('', 10, 'bold'),
              background_color=self.settings['background'], k='Speed')]
    ]
    nameLayout = [
        [sg.T(f"{player.stats['name']}".upper(), font=('', 15, 'bold'),
              background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Level {player.stats['level']}", font=('', 10),
              background_color=self.settings['background'])],
        [sg.ProgressBar(max_value=player.level_up(), bar_color=('#28fc03', '#f2f2f2'),
                        orientation='h', expand_x=True, expand_y=True, relief=sg.RELIEF_RAISED, key='progress_1',)],
    ]
    imageLayout = [
        [sg.Graph((170, 100), (0, 100), (170, 0), p=0, key='GRAPH')]
    ]

    if len(player.stats["type"]) < 2:
        TypeImage2 = [sg.Image(f'Data\\img\\poke\\types\\none.png', k='type2',
                               background_color=self.settings['background'], p=0, size=(30, 24), tooltip=' There is no second type of this Pokemon ')]
    else:
        TypeImage2 = [sg.Image(f'Data\\img\\poke\\types\\{player.stats["type"][1]}_Type_Icon.png', k='type2',
                               background_color=self.settings['background'], p=0, size=(30, 24), tooltip=f' {player.stats["type"][1]} ')]

    conditionBar = [
        [sg.Image(f'Data\\img\\poke\\types\\{player.stats["type"][0]}_Type_Icon.png', k='type1',
                  background_color=self.settings['background'], p=0, size=(30, 24), tooltip=f' {player.stats["type"][0]} ')],
        [sg.HSeparator(color='#3c4754', p=0)],
        TypeImage2,
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.HSeparator(color='#3c4754', p=0)]
    ]

    Column = [
        [sg.Frame('', imageLayout, size=(170, 100), element_justification='center', p=((0, 0), (0, 5)), background_color=self.settings['background']), sg.Frame(
            '', conditionBar, size=(30, 100), element_justification='center', p=((0, 0), (0, 5)), background_color=self.settings['background'])],
        [sg.Frame('', nameLayout, size=(200, 90), element_justification='center', p=(
            (0, 0), (5, 5)), background_color=self.settings['background'])],
        [sg.Frame('', condition_layout, size=(100, 142), element_justification='center', p=((0, 0), (5, 5)), background_color=self.settings['background']), sg.Frame(
            '', condition_values, size=(100, 142), element_justification='center', p=((0, 0), (5, 5)), background_color=self.settings['background'])],
        [sg.Frame('', stats_layout, size=(100, 142), element_justification='center', p=((0, 0), (5, 0)), background_color=self.settings['background']), sg.Frame(
            '', stats_values, size=(100, 142), element_justification='center', p=((0, 0), (5, 0)), background_color=self.settings['background'])]
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
        [sg.B('Main Menu', size=8)],
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


def choosePoke(player):
    layout = [
        [sg.Listbox(values=[x for x in player.open_dex()[0]], enable_events=True,
                    size=(25, 15), key="poke", expand_x=True)],
        [sg.B('Choose', p=((98, 0), (0, 0))), sg.B('Back'), sg.Button(
            'Submit', visible=False, bind_return_key=True)]
    ]

    return layout


def load(player):
    layout = [
        [sg.Listbox(values=[x for x in player.read_save()], enable_events=True,
                    size=(25, 15), key="load", expand_x=True)],
        [sg.B('Load', p=((58, 0), (0, 0))), sg.B('Delete'), sg.B('Back'),
         sg.B('Submit', visible=False, bind_return_key=True)]
    ]

    return layout


def settings(self):
    status1 = 'Enabled' if self.settings['music_playing'] else 'Disabled'
    status2 = 'Enabled' if self.settings['portrait_anim'] else 'Disabled'
    listOfThemes = ['TamagoDefault', 'TamagoDark', 'TamagoLight']
    listOfMusic = ['music1', 'music2', 'music3']

    theme = [
        [sg.T(f"Current theme: {self.settings['theme']}", key='_theme_txt_')],
        [sg.Combo(listOfThemes, size=(25, 10),
                  default_value=f"{self.settings['theme']}", key='_theme_')],
    ]
    sounds = [
        [sg.T(f"Current music: {self.settings['music']}", key='_music_txt_')],
        [sg.Combo(listOfMusic, size=(14, 0), default_value=self.settings['music'],
                  key='_music_'), sg.Checkbox(text=status1, default=self.settings['music_playing'], key='_playing_')],
        [sg.T(f'Music')],
        [sg.Slider(orientation='h', disable_number_display=True,
                   range=(0, 100), default_value=self.settings['music_volume'], key='_music_vol_')],
        [sg.T(f'Sound')],
        [sg.Slider(orientation='h', disable_number_display=True,
                   range=(0, 100), default_value=self.settings['sound_volume'], key='_sound_vol_')]
    ]
    portrait = [
        [sg.T('Animated image:'), sg.Checkbox(
            text=status2, default=self.settings['portrait_anim'], p=((20,0),(0,0)), key='_portrait_')]
    ]
    layout = [
        [sg.Frame('Theme', theme, s=(215, 80))],
        [sg.Frame('Audio', sounds, s=(215, 200))],
        [sg.Frame('Portrait', portrait, s=(215, 55))],
        [sg.B('Apply', p=((133, 0), (5, 0))), sg.B('Back', p=((5, 0), (5, 0)))]
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


def dead2(player):
    layout = [
        [sg.Image('Data\\img\\revive.gif', k='image', p=((20, 20), (20, 0)),)],
        [sg.Text('Your pet is about to begin a new life.',
                 k='text1', p=((0, 0), (20, 0)))],
        [sg.Text(f'The process will take {f.time_counter(player.status["revive_time"])}.', p=(
            (0, 0), (0, 20)), k='text2')],
        [sg.Button('Revive', size=8, k='r'), sg.Button(
            'Let go', size=8, k='l'), sg.Button('Exit', size=8, p=((50, 0), (0, 0)))]
    ]

    return layout


def sleeping(player):
    layout = [
        [sg.Image('Data\\img\\sleep.gif', k='image', p=((20, 20), (0, 0)))],
        [sg.Text('Shhh!!! Your pet is sleeping now.')],
        [sg.Text(f'Let it rest for about {f.time_counter(player.status["sleep_time"])}.', p=(
            (0, 0), (20, 20)), k='text')],
        [sg.Button('Exit', size=8)]
    ]

    return layout


def eating():
    global portion, gif_update

    portion = randint(5, 10)
    gif_update = 'eat'

    layout = [
        [sg.Image('Data\\img\\eat.gif', k='image', p=((20, 20), (20, 20)))],
        [sg.Text(f'You have {portion} portions.', k='text1', p=((0, 0), (20, 0)))],
        [sg.Text("You don't have any food for now!", visible=False, k='text2')],
        [sg.Text("Your pet is full, you can't feed it for now!", visible=False, k='text3')],
        [sg.Button('Give a snack', size=10, k='snack', p=((0, 0), (20, 0))), 
         sg.Button('Serve a meal', size=10, k='meal', p=((0, 0), (20, 0))), 
         sg.Button('Back', size=8, p=((50, 0), (20, 0)))]
    ]

    return layout
