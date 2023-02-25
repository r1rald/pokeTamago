from threading import Thread
import PySimpleGUI as sg
from PIL import Image
import src.hooks.funct as f
import src.components as c
import sys
import os


def sleeping(self,player):
    match self.settings['theme']:

        case "TamagoDefault":
            titlebar = '#283b5b'

        case "TamagoDark":
            titlebar = '#303134'

        case "TamagoLight":
            titlebar = '#0052e7'

    graph = [
        [sg.Graph((300, 260), (0, 260), (300, 0), p=0, key='sleep_graph')],
    ]

    elements = [
        [sg.Frame('', graph, s=(300, 260))],
        [sg.Text('Shhh!!! Your pet is sleeping now.\n' + 
        f'Let it rest for about {f.time_counter(player.status["sleep_time"])}.', k='text', p=(0,10),
        justification='c')],
        [c.button(self,'Main Menu',0.45)]
    ]

    frame = [
        [sg.Frame('', elements, p=(0,0), element_justification="c", relief=sg.RELIEF_FLAT)]
        ]

    layout = [
        [sg.Frame('', frame, p=(0,0), background_color=titlebar, relief=sg.RELIEF_FLAT)]
    ]

    return layout


def sleep_screen(self, player):
    global index1, index2, frames1, frames2, size

    if not player.status['sleeping']:
        player.sleep()

    sleep = True

    def portrait_thread():
        global index1, index2, frames1, frames2
        while True:
            sleep(0.03)
            index1 = (index1 + 1) % frames1
            index2 = (index2 + 1) % frames2
            if not sleep:
                break

    im1 = Image.open(player.properties['portrait'])
    im2 = Image.open('src\\assets\\img\\effects\\sleep.gif')

    width1, height1 = im1.size
    width2, height2 = im2.size

    frames1 = im1.n_frames
    frames2 = im2.n_frames

    graph_width, graph_height = size = (300, 260)

    sleepWindow = sg.Window('Sleeping', sleeping(self,player), finalize=True, size=(320, 375),
        element_justification="c")

    sleepWindow['sleep_graph'].draw_image('src\\assets\\img\\bg\\room_sleeping.png', location=(0, 0))

    index1 = 1
    index2 = 1

    im1.seek(index1)
    im2.seek(index2)

    location1 = (graph_width // 2 - width1 // 2, graph_height // 1.65 - height1 // 1.65)
    location2 = (graph_width // 2 - width1 // 2, graph_height // 2 - (height2 - 10))

    item1 = sleepWindow['sleep_graph'].draw_image(data=f.image2data(im1), location=location1)
    item2 = sleepWindow['sleep_graph'].draw_image(data=f.image2data(im2), location=location2)

    thread = Thread(target=portrait_thread, daemon=True)
    if self.settings['portrait_anim']:
        thread.start()

    while True:
        event, value = sleepWindow.read(timeout=41.66)

        match event:
            case sg.TIMEOUT_KEY:
                im1.seek(index1)
                im2.seek(index2)

                item_new1 = sleepWindow['sleep_graph'].draw_image(data=f.image2data(im1),
                                                                  location=location1)
                item_new2 = sleepWindow['sleep_graph'].draw_image(data=f.image2data(im2),
                                                                  location=location2)

                sleepWindow['sleep_graph'].delete_figure(item1)
                sleepWindow['sleep_graph'].delete_figure(item2)

                item1 = item_new1
                item2 = item_new2

                sleepWindow.refresh()

            case sg.WIN_CLOSED:
                self.run = False
                sys.exit()

            case 'MAIN MENU':
                self.run = False
                os.execl(sys.executable, sys.executable, *sys.argv)

        if player.status['sleeping'] and player.status['sleep_time'] == 0:
            player.status['sleeping'] = False
            break

        sleepWindow['text'].update('Shhh!!! Your pet is sleeping now.\n' +
                                   f'Let it rest for about {f.time_counter(player.status["sleep_time"])}.')

    sleepWindow.close()