from threading import Thread
import PySimpleGUI as sg
from time import sleep
from PIL import Image
import Data.funct as f


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


def train_screen(self, player):
    global index1, index2, index3, frames1, frames2, frames3, size

    train = True

    def portrait_thread():
        global index1, index2, index3, frames1, frames2, frames3
        while True:
            sleep(0.03)
            index1 = (index1 + 1) % frames1
            if player.status['training'] == True:
                index2 = (index2 + 1) % frames2
                index3 = (index3 + 1) % frames3
            if not train:
                break

    im1 = Image.open(player.properties['portrait'])
    im2 = Image.open('data\\img\\effects\\sweat1.gif')
    im3 = Image.open('data\\img\\effects\\sweat2.gif')

    width1, height1 = im1.size
    width2, height2 = im2.size
    width3, height3 = im3.size

    frames1 = im1.n_frames
    frames2 = im2.n_frames
    frames3 = im3.n_frames

    graph_width, graph_height = size = (300, 260)

    trainWindow = sg.Window('Training', training(player), finalize=True, size=(320, 365),
    icon='data\\img\\gym.ico', element_justification="c")

    trainWindow['train_graph'].draw_image('data\\img\\bg\\gym_training.png', location=(0, 0))

    index1 = 1
    index2 = 1
    index3 = 1

    im1.seek(index1)
    im2.seek(index2)
    im3.seek(index3)

    location1 = (graph_width//2-width1//2, graph_height//1.4-height1)
    location2 = ((graph_width//2-width2//2)+60, graph_height//1.4-height1//1.5)
    location3 = ((graph_width//2-width2//2)-60, graph_height//1.4-height1//1.5)

    item1 = trainWindow['train_graph'].draw_image(data=f.image_to_data(im1), location=location1)
    item2 = trainWindow['train_graph'].draw_image(data=f.image_to_data(im2), location=location2)
    item3 = trainWindow['train_graph'].draw_image( data=f.image_to_data(im3), location=location3)

    thread = Thread(target=portrait_thread, daemon=True)
    if self.settings['portrait_anim']:
        thread.start()

    while True:
        event, value = trainWindow.read(timeout=41.66)

        match event:
            case sg.TIMEOUT_KEY:
                trainWindow['train_graph'].delete_figure(item2)
                trainWindow['train_graph'].delete_figure(item3)  

                im1.seek(index1)

                item_new1 = trainWindow['train_graph'].draw_image(data=f.image_to_data(im1),
                location=location1)

                trainWindow['train_graph'].delete_figure(item1)

                item1 = item_new1

                if player.status['training'] == True:
                    im2.seek(index2)
                    im3.seek(index3)
                    item_new2 = trainWindow['train_graph'].draw_image(data=f.image_to_data(im2),
                    location=location2)
                    item_new3 = trainWindow['train_graph'].draw_image(data=f.image_to_data(im3),
                    location=location3)              
                    item2 = item_new2
                    item3 = item_new3

                trainWindow.refresh()

            case sg.WIN_CLOSED | 'Back':
                train = False
                break

            case 'begin':
                player.training()

        if player.status['training'] == True:
            trainWindow['train'].update('Your pokemon is already trained!\n' +
            f'It needs to rest for about {f.time_counter(player.status["training_time"])}')
            trainWindow['begin'].update(disabled=True)

            if player.status['training_time'] == 0:
                player.status['training'] = False
                trainWindow['train'].update('Your pokemon is ready for training!\n'
                + 'Please, be gentle with it!')
                trainWindow['begin'].update(disabled=False)

    trainWindow.close()