from threading import Thread
import PySimpleGUI as sg
from time import sleep
from PIL import Image
import Data.funct as f
import sys
import os


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


def sleep_screen(self, player):
    global index1, index2, frames1, frames2, size

    if not player.status['sleeping']:
        player.sleep()

    sleeping = True

    def portrait_thread():
        global index1, index2, frames1, frames2
        while True:
            sleep(0.03)
            index1 = (index1 + 1) % frames1
            index2 = (index2 + 1) % frames2
            if not sleeping:
                break

    im1 = Image.open(player.properties['portrait'])
    im2 = Image.open('data\\img\\effects\\sleep.gif')

    width1, height1 = im1.size
    width2, height2 = im2.size

    frames1 = im1.n_frames
    frames2 = im2.n_frames

    graph_width, graph_height = size = (300, 260)

    sleepWindow = sg.Window('Sleeping', sleeping(player), finalize=True, size=(320, 375),
                            element_justification="c", icon='data\\img\\sleep.ico')

    sleepWindow['sleep_graph'].draw_image('data\\img\\bg\\room_sleeping.png', location=(0, 0))

    index1 = 1
    index2 = 1

    im1.seek(index1)
    im2.seek(index2)

    location1 = (graph_width // 2 - width1 // 2, graph_height // 1.65 - height1 // 1.65)
    location2 = (graph_width // 2 - width1 // 2, graph_height // 2 - (height2 - 10))

    item1 = sleepWindow['sleep_graph'].draw_image(data=f.image_to_data(im1), location=location1)
    item2 = sleepWindow['sleep_graph'].draw_image(data=f.image_to_data(im2), location=location2)

    thread = Thread(target=portrait_thread, daemon=True)
    if self.settings['portrait_anim']:
        thread.start()

    while True:
        event, value = sleepWindow.read(timeout=41.66)

        match event:
            case sg.TIMEOUT_KEY:
                im1.seek(index1)
                im2.seek(index2)

                item_new1 = sleepWindow['sleep_graph'].draw_image(data=f.image_to_data(im1),
                                                                  location=location1)
                item_new2 = sleepWindow['sleep_graph'].draw_image(data=f.image_to_data(im2),
                                                                  location=location2)

                sleepWindow['sleep_graph'].delete_figure(item1)
                sleepWindow['sleep_graph'].delete_figure(item2)

                item1 = item_new1
                item2 = item_new2

                sleepWindow.refresh()

            case sg.WIN_CLOSED:
                self.run = False
                sys.exit()

            case 'Main Menu':
                self.run = False
                os.execl(sys.executable, sys.executable, *sys.argv)

        if player.status['sleeping'] and player.status['sleep_time'] == 0:
            player.status['sleeping'] = False
            break

        sleepWindow['text'].update('Shhh!!! Your pet is sleeping now.\n' +
                                   f'Let it rest for about {f.time_counter(player.status["sleep_time"])}.')

    sleepWindow.close()