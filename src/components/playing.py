from threading import Thread
import PySimpleGUI as sg
from time import sleep
from PIL import Image
import src.hooks.funct as f
import src.components as c


def play(self):
    match self.settings['theme']:

        case "TamagoDefault":
            titlebar = '#283b5b'

        case "TamagoDark":
            titlebar = '#303134'

        case "TamagoLight":
            titlebar = '#0052e7'

    graph = [
        [sg.Graph((300, 260), (0, 260), (300, 0), p=0, key='play_graph')],
    ]

    elements = [
        [sg.Frame('', graph, s=(300, 260))],
        [sg.Text('Your pet is exhausted, let it rest for now.', visible=False, k='text', p=(0,10))],
        [c.button(self,'Play',0.45), c.button(self,'Back',0.45)]
    ]

    frame = [
        [sg.Frame('', elements, p=(0,0), element_justification="c", relief=sg.RELIEF_FLAT)]
        ]

    layout = [
        [sg.Frame('', frame, p=(0,0), background_color=titlebar, relief=sg.RELIEF_FLAT)]
    ]

    return layout


def play_screen(self, player):
    global index1, index2, frames1, frames2, size, play_button

    playing = True
    play_button = False

    def portrait_thread():
            global index1, index2, frames1, frames2, play_button
            while True:
                sleep(0.03)
                index1 = (index1 + 1) % frames1
                if play_button:
                    index2 = (index2 + 1) % frames2
                    if index2 == 42:
                        play_button = False
                if not playing:
                    break

    im1 = Image.open(player.properties['portrait'])
    im2 = Image.open('src\\assets\\img\\effects\\play.gif')

    width1, height1 = im1.size
    width2, height2 = im2.size

    frames1 = im1.n_frames
    frames2 = im2.n_frames

    graph_width, graph_height = size = (300, 260)

    playWindow = sg.Window('Playing', play(self), size=(320, 375), element_justification="c",
        finalize=True)

    playWindow['play_graph'].draw_image('src\\assets\\img\\bg\\room_playing.png', location=(0, 0))
    playWindow['play_graph'].draw_image('src\\assets\\img\\bg\\room_playing_1.png', location=(0, 0))

    index1 = 1
    index2 = 1

    im1.seek(index1)
    im2.seek(index2)

    location1 = (graph_width//2-width1//2, graph_height//1.5-height1)
    location2 = ((graph_width//2-width2//2)+width1//2, (graph_height//1.5-height2//2)-height1)

    item1 = playWindow['play_graph'].draw_image(data=f.image2data(im1), location=location1)
    item2 = playWindow['play_graph'].draw_image(data=f.image2data(im2), location=location2)

    thread = Thread(target=portrait_thread, daemon=True)
    if self.settings['portrait_anim']:
        thread.start()

    playWindow['play_graph'].draw_image('src\\assets\\img\\bg\\room_playing_2.png', location=(0, 0))

    while True:
        event, value = playWindow.read(timeout=24)

        match event:
            case sg.TIMEOUT_KEY:
                playWindow['play_graph'].delete_figure(item2)

                im1.seek(index1)
                
                item_new1 = playWindow['play_graph'].draw_image(data=f.image2data(im1),
                location=location1)

                playWindow['play_graph'].delete_figure(item1)

                item1 = item_new1

                if play_button:
                    im2.seek(index2)
                    item_new2 = playWindow['play_graph'].draw_image(data=f.image2data(im2),
                    location=location2)
                    item2 = item_new2

                playWindow.refresh()

            case sg.WINDOW_CLOSED | 'BACK':
                playing = False
                break

            case 'PLAY':
                player.play()

                if player.condition['exhausted'] < 90:
                    play_button = True
                
                    if play_button and index2 > 1:
                        index2 = 1

        if player.condition['exhausted'] >= 90:
            playWindow['text'].update(visible=True)
            playWindow['PLAY'].update(disabled=True)
        else:
            playWindow['text'].update(visible=False)
            playWindow['PLAY'].update(disabled=False)

    playWindow.close()
