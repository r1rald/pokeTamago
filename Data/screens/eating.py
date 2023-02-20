from threading import Thread
import PySimpleGUI as sg
from time import sleep
from PIL import Image
import Data.funct as f


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


def eat_screen(self, player):
    global index1, index2, frames1, frames2, size

    eating = True

    def portrait_thread():
            global index1, index2, frames1, frames2
            while True:
                sleep(0.03)
                index1 = (index1 + 1) % frames1
                if player.status['eating'] == True:
                    index2 = (index2 + 1) % frames2
                if not eating:
                    break

    im1 = Image.open(player.properties['portrait'])
    im2 = Image.open('data\\img\\effects\\eat.gif')

    width1, height1 = im1.size
    width2, height2 = im2.size

    frames1 = im1.n_frames
    frames2 = im2.n_frames

    graph_width, graph_height = size = (300, 260)

    eatWindow = sg.Window('Eating', eating(player), finalize=True, size=(320, 375),
    element_justification="c", icon='data\\img\\eat.ico')

    eatWindow['eat_graph'].draw_image('data\\img\\bg\\kitchen_eating.png', location=(0, 0))

    index1 = 1
    index2 = 1

    im1.seek(index1)
    im2.seek(index2)

    location1 = (graph_width//2-width1//2, graph_height//1.5-height1)
    location2 = (graph_width//2-width2//2, graph_height//1.5-(height2+(height1//2)))

    item1 = eatWindow['eat_graph'].draw_image(data=f.image_to_data(im1), location=location1)
    item2 = eatWindow['eat_graph'].draw_image(data=f.image_to_data(im2), location=location2)

    thread = Thread(target=portrait_thread, daemon=True)
    if self.settings['portrait_anim']:
        thread.start()

    while True:
        event, value = eatWindow.read(timeout=41.66)

        match event:
            case sg.TIMEOUT_KEY:
                eatWindow['eat_graph'].delete_figure(item2)

                im1.seek(index1)
                
                item_new1 = eatWindow['eat_graph'].draw_image(data=f.image_to_data(im1),
                location=location1)

                eatWindow['eat_graph'].delete_figure(item1)

                item1 = item_new1

                if player.status['eating'] == True:
                    im2.seek(index2)
                    item_new2 = eatWindow['eat_graph'].draw_image(data=f.image_to_data(im2),
                    location=location2)
                    item2 = item_new2

                eatWindow.refresh()

            case sg.WINDOW_CLOSED | 'Back':
                eating = False
                break

            case 'feed':
                player.eat()

        if player.status['eating']:
            eatWindow['text1'].update(visible=False)
            eatWindow['text3'].update("Your pet is full, you can't feed it for now!\n" + 
            f'Let it rest for about {f.time_counter(player.status["eat_time"])}.', visible=True)
            eatWindow['feed'].update(disabled=True)
            if player.status['eat_time'] == 0:
                player.status['eating'] = False
                eatWindow['text1'].update(visible=True)
                eatWindow['text3'].update(visible=False)
                eatWindow['feed'].update(disabled=False)

    eatWindow.close()