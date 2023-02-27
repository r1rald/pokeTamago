import src.components as c
import PySimpleGUI as sg
from re import sub, search
from PIL import Image
import src.hooks.funct as f
from time import sleep
from threading import Thread


def choosePoke(self,player):
    match self.settings['theme']:

        case "TamagoDefault":
            titlebar = '#283b5b'
            bg = '#516173'

        case "TamagoDark":
            titlebar = '#303134'
            bg = '#303134'

        case "TamagoLight":
            titlebar = '#0052e7'
            bg = '#0052e7'

    nameLayout = [
        [sg.Text(f'{player.properties["name"].upper()}', p=0, background_color=bg,
             font=('Pokemon Pixel Font',16,'bold'), text_color='white')]
    ]

    imageLayout = [
        [sg.Graph((170, 100), (0, 100), (170, 0), p=0, key='GRAPH')]
    ]

    elements = [
        [sg.Frame('', nameLayout, size=(170, 23), p=((5,5),(5,0)), element_justification='c', 
            background_color=bg)],
        [sg.Frame('', imageLayout, size=(170, 100), p=((5,5),(0,0)), element_justification='c')],
        [sg.Listbox(values=[f'{self.open_dex()[0].index(x)+1}. {x}' for x in self.open_dex()[0]], 
            p=((5,5),(0,0)), enable_events=True, size=(19, 10), key="poke", expand_x=True,)], 
        [sg.Input(key='-IN-', s=28, expand_x=False, expand_y=False, justification='l',
            font=('Pokemon Pixel Font', 16, 'normal'), p=((5,5),(0,10)), border_width=1)],
        [c.button(self,'Choose',0.5,pad=((0,5),(0,5))), c.button(self,'Back',0.5,pad=((5,0),(0,5)))]
    ]

    frame = [
        [sg.Frame('', elements, p=0, element_justification="c", relief=sg.RELIEF_FLAT)]
        ]

    layout = [
        [sg.Frame('', frame, p=0, background_color=titlebar, relief=sg.RELIEF_FLAT)]
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

                            name = sub("\s|[']|[.0-9]", '', values["poke"][0])
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
                    name = sub("\s|[']|[.0-9]", '', values["poke"][0])
                    index = self.open_dex()[0].index(name)

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

        if values['-IN-']:
            pokeChooseWin['poke'].update(
                values=[f'{self.open_dex()[0].index(x)+1}. {x}' for x in self.open_dex()[0] if search(
                    f'(?i)(?:{values["-IN-"]})', x)]
                )
        else:
            pokeChooseWin['poke'].update(
                values=[f'{self.open_dex()[0].index(x)+1}. {x}' for x in self.open_dex()[0]]
                )


    pokeChooseWin.close()