import src.hooks.funct as f
import src.components as c
import PySimpleGUI as sg

def main_loop(self, player):   
    condition_layout = [
        [sg.T("Health", font=('', 10, 'bold'))], [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T("Age", font=('', 10, 'bold'))], [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Food", font=('', 10, 'bold'))], [sg.HSeparator(color='#3c4754', p=0)], 
        [sg.T(f"Bored", font=('', 10, 'bold'))], [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Exhausted", font=('', 10, 'bold'))]
    ]

    condition_values = [
        [sg.T(f"{int(player.condition['health'])}", font=('', 10, 'bold'), k='health')],
        [sg.HSeparator(color='#3c4754', p=0)], 
        [sg.T(f"{f.time_counter(player.condition['age'])}", font=('', 10, 'bold'), k='age')],
        [sg.HSeparator(color='#3c4754', p=0)], 
        [sg.ProgressBar(max_value=100, orientation='h', p=0, key='food',)], 
        [sg.HSeparator(color='#3c4754', p=0)], 
        [sg.ProgressBar(max_value=100, orientation='h', p=0, key='bored',)], 
        [sg.HSeparator(color='#3c4754', p=0)], 
        [sg.ProgressBar(max_value=100, orientation='h', p=0, key='exhausted',)]
    ]

    stats_layout = [
        [sg.T(f"Attack", font=('', 10, 'bold'))], [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Defense", font=('', 10, 'bold'))], [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Sp. Attack", font=('', 10, 'bold'))], [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Sp. Defense", font=('', 10, 'bold'))], [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Speed", font=('', 10, 'bold'))]
    ]

    stats_values = [
        [sg.T(f"{int(player.base['Attack'])}", font=('', 10, 'bold'), k='Attack')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{int(player.base['Defense'])}", font=('', 10, 'bold'), k='Defense')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{int(player.base['Sp. Attack'])}", font=('', 10, 'bold'), k='Sp. Attack')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{int(player.base['Sp. Defense'])}", font=('', 10, 'bold'), k='Sp. Defense')],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"{int(player.base['Speed'])}", font=('', 10, 'bold'), k='Speed')]
    ]

    nameLayout = [
        [sg.T(f"{player.properties['name']}".upper(), font=('', 15, 'bold'))],
        [sg.HSeparator(color='#3c4754', p=0)],
        [sg.T(f"Level {player.properties['level']}", font=('', 10), key='level')],
        [sg.ProgressBar(max_value=player.xp_need(), expand_x=True, expand_y=True, orientation='h',
        key='progress_1')],
    ]

    imageLayout = [
        [sg.Graph((170, 100), (0, 100), (170, 0), p=0, key='GRAPH')]
    ]

    if len(player.properties["type"]) < 2:
        TypeImage2 = [
            sg.Image(f'src\\assets\\img\\types\\none.png', k='type2', p=0, size=(30, 24), 
            tooltip=' There is no second type of this Pokemon ')
        ]
    else:
        TypeImage2 = [
            sg.Image(f'src\\assets\\img\\types\\{player.properties["type"][1]}_Type_Icon.png', k='type2',
            p=0,  size=(30, 24), tooltip=f' {player.properties["type"][1]} ')
        ]

    conditionBar = [
        [sg.Image(f'src\\assets\\img\\types\\{player.properties["type"][0]}_Type_Icon.png', k='type1',
        p=0, size=(30, 24), tooltip=f' {player.properties["type"][0]} ')], [sg.HSeparator(color='#3c4754', p=0)],
        TypeImage2, [sg.HSeparator(color='#3c4754', p=0)], [sg.HSeparator(color='#3c4754', p=0)]
    ]

    Column = [
        [sg.Frame('', imageLayout, size=(170, 100), element_justification='c', p=((0, 0), (0, 5))),
         sg.Frame('', conditionBar, size=(30, 100), element_justification='c', p=((0, 0), (0, 5)))],
        [sg.Frame('', nameLayout, size=(200, 90), element_justification='c', p=((0, 0), (5, 5)))],
        [sg.Frame('', condition_layout, size=(100, 142), element_justification='c', p=((0, 0), (5, 5))), 
         sg.Frame('', condition_values, size=(100, 142), element_justification='c', p=((0, 0), (5, 5)))],
        [sg.Frame('', stats_layout, size=(100, 142), element_justification='c', p=((0, 0), (5, 0))),
         sg.Frame('', stats_values, size=(100, 142), element_justification='c', p=((0, 0), (5, 0)))]
    ]

    buttonColumn = [
        [c.button(self,'Eat',0.6)],
        [c.button(self,'Play',0.6)],
        [c.button(self,'Sleep',0.6)],
        [sg.HSeparator(color='#3c4754', p=((0, 0), (10, 10)))],
        [c.button(self,'Training',0.6)],
        [c.button(self,'Battle',0.6,True)],
        [c.button(self,'Shop',0.6,True)],
        [sg.HSeparator(color='#3c4754', p=((0, 0), (10, 10)))],
        [c.button(self,'Main Menu',0.6)]
    ]

    elements = [
        [sg.Column(buttonColumn), sg.Column(Column, element_justification='c')],
    ]

    return elements