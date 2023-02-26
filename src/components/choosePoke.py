import src.components as c
import PySimpleGUI as sg
from re import sub
from PIL import Image
import src.hooks.funct as f
from time import sleep
from threading import Thread


def choosePoke(self,player):
    match self.settings['theme']:

        case "TamagoDefault":
            titlebar = '#283b5b'

        case "TamagoDark":
            titlebar = '#303134'

        case "TamagoLight":
            titlebar = '#0052e7'

    nameLayout = [
        [sg.Text(f'{player.properties["name"].upper()}', p=0, font=('',10,'bold'))]
    ]

    imageLayout = [
        [sg.Graph((170, 100), (0, 100), (170, 0), p=0, key='GRAPH')]
    ]

    elements = [
        [sg.Frame('', nameLayout, size=(170, 23), p=0, element_justification='c')],
        [sg.Frame('', imageLayout, size=(170, 100), p=0, element_justification='c')],
        [sg.Listbox(values=[x for x in self.open_dex()[0]], p=0, enable_events=True, size=(25, 15), 
            key="poke", expand_x=True,)], 
        [c.button(self,'Choose',0.45), c.button(self,'Back',0.45)]
    ]

    frame = [
        [sg.Frame('', elements, p=(0,0), element_justification="c", relief=sg.RELIEF_FLAT)]
        ]

    layout = [
        [sg.Frame('', frame, p=(0,0), background_color=titlebar, relief=sg.RELIEF_FLAT)]
    ]

    return layout


def choose_pokemon(self, player):
    global index, frames, size

    poke_choosed = True

    def portrait_thread():
        global index, frames
        while True:
            sleep(0.03)
            index = (index + 1) % frames
            if not poke_choosed:
                break

    im = Image.open('src\\assets\\img\\poke\\default.gif')

    width, height = im.size
    frames = im.n_frames

    graph_width, graph_height = size = (170, 100)

    pokeChooseWin = sg.Window('Choose', choosePoke(self,player), finalize=True)

    pokeChooseWin['GRAPH'].draw_image('src\\assets\\img\\bg\\grassland-feild-day.png', location=(0, 0))

    index = 1

    im.seek(index)

    location = (graph_width//2-width//2, graph_height//2-height//2)

    item = pokeChooseWin['GRAPH'].draw_image(data=f.image2data(im),location=location)

    thread = Thread(target=portrait_thread, daemon=True)
    if self.settings['portrait_anim']:
        thread.start()

    while True:
        event, values = pokeChooseWin.read(timeout=24)

        pokeChooseWin["poke"].bind('<Double-Button-1>', "+-double click-")

        match event:
            case sg.TIMEOUT_KEY:
                    try:
                        if values['poke']:
                            pokeChooseWin['GRAPH'].delete_figure(item)

                            name = sub("\s|[']", '', values["poke"][0])
                            im = Image.open(f'src\\assets\\img\\poke\\{name}.gif')

                            width, height = im.size
                            frames = im.n_frames

                            location = (graph_width//2-width//2, graph_height//2-height//2)

                            item = pokeChooseWin['GRAPH'].draw_image(data=f.image2data(im),location=location)

                        im.seek(index)

                        item_new = pokeChooseWin['GRAPH'].draw_image(data=f.image2data(im),
                            location=location)
                        
                        pokeChooseWin['GRAPH'].delete_figure(item)

                        item = item_new
                    except EOFError:
                        pass

                    pokeChooseWin.refresh()

            case sg.WINDOW_CLOSED | 'BACK':
                player.properties['name'] = ""
                break

            case 'CHOOSE' | 'poke+-double click-':
                if values['poke']:
                    index = self.open_dex()[0].index(f'{values["poke"][0]}')

                    name = sub("\s|[']", '', values["poke"][0])

                    player.properties['portrait'] = f'src\\assets\\img\\poke\\{name}.gif'
                    player.properties['type'] = self.open_dex()[1][index]
                    player.properties['xp_group'] = self.open_dex()[2][index]
                    player.properties['yield'] = self.open_dex()[3][index]

                    self.cancel = True
                    break

                else:
                    event = c.popUp(self,'','You must choose a Pokemon!', True)

                    if event == 'OK':
                        continue

    pokeChooseWin.close()