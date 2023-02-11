import PySimpleGUI as sg
import funct as f


def newGame():
    buttonColumn = [
        [sg.Button('New Pokemon', size=12)],
        [sg.Button('Continue', size=12, key='load')],
        [sg.B('Settings', size=12)],
        [sg.B('Exit', size=12)]
    ]

    layout = [
        [sg.Image('data\\img\\logo.png', subsample=3)],
        [sg.Column(buttonColumn, element_justification='c')]
    ]

    return layout


def mainGame(self, player):
    condition_layout = [
        [sg.T("Health", font=('', 10, 'bold'), background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T("Age", font=('', 10, 'bold'), background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Food", font=('', 10, 'bold'), background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Bored", font=('', 10, 'bold'), background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Exhausted", font=('', 10, 'bold'), background_color=self.settings['background'])]
    ]

    condition_values = [
        [sg.T(f"{int(player.condition['health'])}", font=('', 10, 'bold'), k='health', 
        background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T("", font=('', 10, 'bold'), k='age', background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.ProgressBar(max_value=100, orientation='h', expand_x=True, expand_y=True, p=0,
        key='food',)],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.ProgressBar(max_value=100, orientation='h', expand_x=True, expand_y=True, p=0,
        key='bored',)],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.ProgressBar(max_value=100, orientation='h', expand_x=True, expand_y=True, p=0,
        key='exhausted',)]
    ]

    stats_layout = [
        [sg.T(f"Attack", font=('', 10, 'bold'), background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Defense", font=('', 10, 'bold'), background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Sp. Attack", font=('', 10, 'bold'), background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Sp. Defense", font=('', 10, 'bold'), background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Speed", font=('', 10, 'bold'), background_color=self.settings['background'])]
    ]

    stats_values = [
        [sg.T(f"{player.base['Attack']}", font=('', 10, 'bold'), background_color=self.settings['background'],
        k='Attack')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{player.base['Defense']}", font=('', 10, 'bold'), background_color=self.settings['background'],
        k='Defense')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{player.base['Sp. Attack']}", font=('', 10, 'bold'), background_color=self.settings['background'],
        k='Sp. Attack')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{player.base['Sp. Defense']}", font=('', 10, 'bold'), background_color=self.settings['background'],
        k='Sp. Defense')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{player.base['Speed']}", font=('', 10, 'bold'), background_color=self.settings['background'],
        k='Speed')]
    ]

    nameLayout = [
        [sg.T(f"{player.properties['name']}".upper(), font=('', 15, 'bold'), 
        background_color=self.settings['background'])],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Level {player.properties['level']}", font=('', 10), key='level',
        background_color=self.settings['background'])],
        [sg.ProgressBar(max_value=player.xp_need(), expand_x=True, expand_y=True, key='progress_1',
        orientation='h', bar_color=('#28fc03','#f2f2f2'), relief=sg.RELIEF_RAISED)],
    ]

    imageLayout = [
        [sg.Graph((170, 100), (0, 100), (170, 0), p=0, key='GRAPH')]
    ]

    if len(player.properties["type"]) < 2:
        TypeImage2 = [
            sg.Image(f'data\\img\\types\\none.png', k='type2', p=0, size=(30, 24), 
            background_color=self.settings['background'], tooltip=' There is no second type of this Pokemon ')
        ]
    else:
        TypeImage2 = [
            sg.Image(f'data\\img\\types\\{player.properties["type"][1]}_Type_Icon.png', k='type2',
            background_color=self.settings['background'], p=0,  size=(30, 24), tooltip=f' {player.properties["type"][1]} ')
        ]

    conditionBar = [
        [sg.Image(f'data\\img\\types\\{player.properties["type"][0]}_Type_Icon.png', k='type1',
        background_color=self.settings['background'], p=0, size=(30, 24), tooltip=f' {player.properties["type"][0]} ')],
        [sg.HSeparator(color='#3c4754', p=0)],
        TypeImage2,
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.HSeparator(color='#3c4754', p=0)]
    ]

    Column = [
        [sg.Frame('', imageLayout, size=(170, 100), element_justification='c', p=((0, 0), (0, 5)),
        background_color=self.settings['background']),
        sg.Frame('', conditionBar, size=(30, 100), element_justification='c', p=((0, 0), (0, 5)),
        background_color=self.settings['background'])],
        [sg.Frame('', nameLayout, size=(200, 90), element_justification='c', p=((0, 0), (5, 5)),
        background_color=self.settings['background'])],
        [sg.Frame('', condition_layout, size=(100, 142), element_justification='c', p=((0, 0), (5, 5)),
        background_color=self.settings['background']), 
        sg.Frame('', condition_values, size=(100, 142), element_justification='c', p=((0, 0), (5, 5)),
        background_color=self.settings['background'])],
        [sg.Frame('', stats_layout, size=(100, 142), element_justification='c', p=((0, 0), (5, 0)),
        background_color=self.settings['background']),
        sg.Frame('', stats_values, size=(100, 142), element_justification='c', p=((0, 0), (5, 0)),
        background_color=self.settings['background'])]
    ]

    buttonColumn = [
        [sg.B('Eat', size=8)],
        [sg.B('Play', size=8)],
        [sg.B('Sleep', size=8)],
        [sg.HSeparator(color='#3c4754', p=((0, 0), (10, 10)))],
        [sg.B('Training', size=8)],
        [sg.B('Battle', size=8, disabled=True)],
        [sg.B('Shop', size=8, disabled=True)],
        [sg.HSeparator(color='#3c4754', p=((0, 0), (10, 10)))],
        [sg.B('Main Menu', size=8)],
    ]

    layout = [
        [sg.Column(buttonColumn), sg.Column(Column, element_justification='c')],
    ]

    return layout


def newPoke():
    layout = [
        [sg.Text('What is the name of your Pokemon?')],
        [sg.Input(key='-IN-')],
        [sg.B('Random'), sg.Button('Enter', p=((170, 0), (0, 0))), 
        sg.Button('Back'),sg.Button('Submit', visible=False, bind_return_key=True)]
    ]

    return layout


def choosePoke(self):
    layout = [
        [sg.Listbox(values=[x for x in self.open_dex()[0]], enable_events=True, size=(25, 15), 
        key="poke", expand_x=True,)],
        [sg.B('Choose', p=((98, 0), (0, 0))), sg.B('Back')]
    ]

    return layout


def load(self):
    layout = [
        [sg.Listbox(values=[x for x in self.read_save()], enable_events=True, expand_y=True, 
        expand_x=True, key="load")],
        [sg.B('Load', p=((55, 0), (0, 0))), sg.B('Delete'), sg.B('Back'), 
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
        [sg.Combo(listOfThemes, size=(25, 10), default_value=f"{self.settings['theme']}", key='_theme_')],
    ]

    sounds = [
        [sg.T(f"Current music: {self.settings['music']}", key='_music_txt_')],
        [sg.Combo(listOfMusic, size=(14, 0), default_value=self.settings['music'], key='_music_'),
        sg.Checkbox(text=status1, default=self.settings['music_playing'], key='_playing_')],
        [sg.T(f'Music')],
        [sg.Slider(orientation='h', disable_number_display=True,range=(0, 100), key='_music_vol_',
        default_value=self.settings['music_volume'])],
        [sg.T(f'Sound')],
        [sg.Slider(orientation='h', disable_number_display=True, range=(0, 100), key='_sound_vol_',
        default_value=self.settings['sound_volume'])]
    ]

    portrait = [
        [sg.T('Animated image:'), sg.Checkbox(text=status2, default=self.settings['portrait_anim'],
        p=((20, 0), (0, 0)), key='_portrait_')]
    ]

    layout = [
        [sg.Frame('Theme', theme, s=(215, 80))],
        [sg.Frame('Audio', sounds, s=(215, 200))],
        [sg.Frame('Portrait', portrait, s=(215, 55))],
        [sg.B('Default', p=((5, 0), (10, 5))), sg.B('Apply', p=((73, 0), (10, 5))),
        sg.B('Back', p=((10, 0), (10, 5)))]
    ]

    return layout


def dead(player):
    graph1 = [
        [sg.Graph((300, 260), (0, 260), (300, 0), p=0, key='death_graph')],
    ]
    graph2 =[
        [sg.Graph((300, 260), (0, 260), (300, 0), p=0, key='revive_graph')]
    ]

    layout = [
        [sg.Frame('', graph1, s=(300, 260), visible=True, k='death_frame'), sg.Frame('', graph2,
        s=(300, 260), visible=False, k='revive_frame')],
        [sg.Text('Sadly seems like your pet is passed away.\n Do you want to revive it?',
        p=(0,10), k='text1', visible=True, justification='c')],
        [sg.Text('Your pet is about to begin a new life.\n' +
        f'The process will take {f.time_counter(player.status["revive_time"])}.', p=(0,10),
        visible=False, k='text2', justification='c')], [sg.Button('Revive', size=8, k='revive', 
        p=(0,10), visible=True), sg.Button('Letting go', size=8, k='letgo', p=(0,10), visible=True),
        sg.Button('Main Menu', size=8, p=(0, 10), k='menu', visible=False)]
    ]

    return layout


def training(player):
    graph = [
        [sg.Graph((300, 260), (0, 260), (300, 0), p=0, key='train_graph')],
    ]

    layout = [
        [sg.Frame('', graph, s=(300, 260))],
        [sg.T('Your pokemon is ready for training!\nPlease, be gentle with it!', justification='c',
        k='train')],
        [sg.B("Let's begin", p=(10, 10), k='begin'), sg.B('Back', p=(10, 10))]
    ]

    return layout


def sleeping(player):
    graph = [
        [sg.Graph((300, 260), (0, 260), (300, 0), p=0, key='sleep_graph')],
    ]

    layout = [
        [sg.Frame('', graph, s=(300, 260))],
        [sg.Text('Shhh!!! Your pet is sleeping now.\n' + 
        f'Let it rest for about {f.time_counter(player.status["sleep_time"])}.', k='text', p=(0,10),
        justification='c')],
        [sg.Button('Main Menu', size=8, p=(0,10))]
    ]

    return layout


def eating(player):
    graph = [
        [sg.Graph((300, 260), (0, 260), (300, 0), p=0, key='eat_graph')],
    ]

    layout = [
        [sg.Frame('', graph, s=(300, 260))],
        [sg.Text('Your pet is hungry and waiting to be fed.', visible=True, k='text1', p=(0,10)), 
        sg.Text("You don't have any food for now!", visible=False, k='text2', p=(0,10)),
        sg.Text("Your pet is full, you can't feed it for now!\n" +
        f'Let it rest for about {f.time_counter(player.status["eat_time"])}.', justification='c',
        visible=False, k='text3', p=(0,10))],
        [sg.Button('Feed', size=8, p=(10,10), k='feed'), sg.Button('Back', size=8, p=(10,10))]
    ]

    return layout


def playing():
    graph = [
        [sg.Graph((300, 260), (0, 260), (300, 0), p=0, key='play_graph')],
    ]

    layout = [
        [sg.Frame('', graph, s=(300, 260))],
        [sg.Text('Your pet is exhausted, let it rest for now.', visible=False, k='text', p=(0,10))],
        [sg.B('Play', p=(0,10), disabled=False, k='play'), sg.B('Back')]
    ]

    return layout
