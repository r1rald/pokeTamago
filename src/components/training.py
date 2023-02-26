from threading import Thread
import PySimpleGUI as sg
from time import sleep
from PIL import Image
import src.hooks.funct as f
import src.components as c


def training(self):
    match self.settings['theme']:

        case "TamagoDefault":
            titlebar = '#283b5b'

        case "TamagoDark":
            titlebar = '#303134'

        case "TamagoLight":
            titlebar = '#0052e7'

    graph = [
        [sg.Graph((300, 260), (0, 260), (300, 0), p=0, key='train_graph')],
    ]

    elements = [
        [sg.Frame('', graph, s=(300, 260))],
        [sg.T('Your pokemon is ready for training!\nPlease, be gentle with it!', justification='c',
        k='train')],
        [c.button(self,"Let's begin",0.45), c.button(self,'Back',0.45)]
    ]

    frame = [
        [sg.Frame('', elements, p=(0,0), element_justification="c", relief=sg.RELIEF_FLAT)]
        ]

    layout = [
        [sg.Frame('', frame, p=(0,0), background_color=titlebar, relief=sg.RELIEF_FLAT)]
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
    im2 = Image.open('src\\assets\\img\\effects\\sweat1.gif')
    im3 = Image.open('src\\assets\\img\\effects\\sweat2.gif')

    width1, height1 = im1.size
    width2, height2 = im2.size
    width3, height3 = im3.size

    frames1 = im1.n_frames
    frames2 = im2.n_frames
    frames3 = im3.n_frames

    graph_width, graph_height = size = (300, 260)

    trainWindow = sg.Window('Training', training(self), size=(320, 365), element_justification="c",
        finalize=True)

    trainWindow['train_graph'].draw_image('src\\assets\\img\\bg\\gym_training.png', location=(0, 0))

    index1 = 1
    index2 = 1
    index3 = 1

    im1.seek(index1)
    im2.seek(index2)
    im3.seek(index3)

    location1 = (graph_width//2-width1//2, graph_height//1.4-height1)
    location2 = ((graph_width//2-width2//2)+60, graph_height//1.4-height1//1.5)
    location3 = ((graph_width//2-width2//2)-60, graph_height//1.4-height1//1.5)

    item1 = trainWindow['train_graph'].draw_image(data=f.image2data(im1), location=location1)
    item2 = trainWindow['train_graph'].draw_image(data=f.image2data(im2), location=location2)
    item3 = trainWindow['train_graph'].draw_image( data=f.image2data(im3), location=location3)

    thread = Thread(target=portrait_thread, daemon=True)
    if self.settings['portrait_anim']:
        thread.start()

    while True:
        event, value = trainWindow.read(timeout=24)

        match event:
            case sg.TIMEOUT_KEY:
                trainWindow['train_graph'].delete_figure(item2)
                trainWindow['train_graph'].delete_figure(item3)  

                im1.seek(index1)

                item_new1 = trainWindow['train_graph'].draw_image(data=f.image2data(im1),
                location=location1)

                trainWindow['train_graph'].delete_figure(item1)

                item1 = item_new1

                if player.status['training'] == True:
                    im2.seek(index2)
                    im3.seek(index3)
                    item_new2 = trainWindow['train_graph'].draw_image(data=f.image2data(im2),
                    location=location2)
                    item_new3 = trainWindow['train_graph'].draw_image(data=f.image2data(im3),
                    location=location3)              
                    item2 = item_new2
                    item3 = item_new3

                trainWindow.refresh()

            case sg.WIN_CLOSED | 'BACK':
                train = False
                break

            case "LET'S BEGIN":
                player.training()

        if player.status['training'] == True:
            trainWindow['train'].update('Your pokemon is already trained!\n' +
            f'It needs to rest for about {f.time_counter(player.status["training_time"])}')
            trainWindow["LET'S BEGIN"].update(disabled=True)

            if player.status['training_time'] == 0:
                player.status['training'] = False
                trainWindow['train'].update('Your pokemon is ready for training!\n'
                + 'Please, be gentle with it!')
                trainWindow["LET'S BEGIN"].update(disabled=False)

    trainWindow.close()