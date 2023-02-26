from threading import Thread
import PySimpleGUI as sg
from time import sleep
from PIL import Image
import src.hooks.funct as f
import src.components as c
import sys
import os


def dead(self,player):
    match self.settings['theme']:

        case "TamagoDefault":
            titlebar = '#283b5b'

        case "TamagoDark":
            titlebar = '#303134'

        case "TamagoLight":
            titlebar = '#0052e7'

    graph1 = [
        [sg.Graph((300, 260), (0, 260), (300, 0), p=0, key='death_graph')],
    ]
    graph2 =[
        [sg.Graph((300, 260), (0, 260), (300, 0), p=0, key='revive_graph')]
    ]

    elements = [
        [sg.Frame('', graph1, s=(300, 260), visible=True, k='death_frame'), 
         sg.Frame('', graph2, s=(300, 260), visible=False, k='revive_frame')],
        [sg.Text('Sadly seems like your pet is passed away.\n Do you want to revive it?',
            p=(0,10), k='text1', visible=True, justification='c')],
        [sg.Text('Your pet is about to begin a new life.\n' +
            f'The process will take {f.time_counter(player.status["revive_time"])}.', p=(0,10),
            visible=False, k='text2', justification='c')], 
        [c.button(self,'Revive',0.45), c.button(self,'Letting go',0.45),
         c.button(self,'Main Menu',0.45,False,False)]
    ]

    frame = [
        [sg.Frame('', elements, p=(0,0), element_justification="c", relief=sg.RELIEF_FLAT)]
        ]

    layout = [
        [sg.Frame('', frame, p=(0,0), background_color=titlebar, relief=sg.RELIEF_FLAT)]
    ]

    return layout


def death_screen(self, player):
    global index1, index2, index3, frames1, frames2, frames3, size

    death = True

    def portrait_thread():
        global index1, index2, index3, frames1, frames2, frames3
        while True:
            sleep(0.03)
            index1 = (index1 + 1) % frames1
            index2 = (index2 + 1) % frames2
            if player.status["revive"]:
                index1 = (index1 + 1) % frames1
                index3 = (index3 + 1) % frames3
            if not death:
                break

    im1 = Image.open(player.properties['portrait'])
    im2 = Image.open('src\\assets\\img\\effects\\death.gif')
    im3 = Image.open('src\\assets\\img\\effects\\revive.gif')

    width1, height1 = im1.size
    width2, height2 = im2.size
    width3, height3 = im3.size

    frames1 = im1.n_frames
    frames2 = im2.n_frames
    frames3 = im3.n_frames

    graph_width, graph_height = size = (300, 260)

    deathWindow = sg.Window('Passing', dead(self,player), finalize=True, element_justification="c")

    deathWindow['death_graph'].draw_image('src\\assets\\img\\bg\\death_graveyard.png', location=(0, 0))
    deathWindow['revive_graph'].draw_image('src\\assets\\img\\death_graveyard.png', location=(0, 0))

    index1 = 1
    index2 = 1
    index3 = 1

    im1.seek(index1)
    im2.seek(index2)
    im3.seek(index3)

    location1 = (graph_width//2-width1//2, graph_height//1.4-height1)
    location2 = ((graph_width//2-width2//2), (graph_height//1.4-height1)-height1)
    location3 = ((graph_width//2-width3//2), (graph_height//1.4-height1)-height1)

    item1 = deathWindow['death_graph'].draw_image(data=f.image2data(im1), location=location1)
    item2 = deathWindow['death_graph'].draw_image(data=f.image2data(im2), location=location2)
    item3 = deathWindow['revive_graph'].draw_image(data=f.image2data(im1), location=location1)
    item4 = deathWindow['revive_graph'].draw_image(data=f.image2data(im3), location=location3)

    thread = Thread(target=portrait_thread, daemon=True)
    if self.settings['portrait_anim']:
        thread.start()

    while True:
        event, value = deathWindow.read(timeout=24)

        match event:
            case sg.TIMEOUT_KEY:
                deathWindow['death_graph'].delete_figure(item1)
                deathWindow['death_graph'].delete_figure(item2)
                deathWindow['revive_graph'].delete_figure(item3)
                deathWindow['revive_graph'].delete_figure(item4)

                im1.seek(index1)
                im2.seek(index2)

                item_new1 = deathWindow['death_graph'].draw_image(data=f.image2data(im1),
                location=location1)
                item_new2 = deathWindow['death_graph'].draw_image(data=f.image2data(im2),
                location=location2)

                item1 = item_new1
                item2 = item_new2

                if player.status["revive"]:
                    im1.seek(index1)
                    im3.seek(index3)
                    item_new3 = deathWindow['revive_graph'].draw_image(data=f.image2data(im1),
                    location=location1)
                    item_new4 = deathWindow['revive_graph'].draw_image(data=f.image2data(im3),
                    location=location2)
                    item3 = item_new3
                    item4 = item_new4

                deathWindow.refresh()

            case sg.WIN_CLOSED:
                self.run = False
                death = False
                sys.exit()

            case 'MENU':
                self.run = False
                death = False
                os.execl(sys.executable, sys.executable, *sys.argv)

            case 'REVIVE':
                player.status['revive'] = True
                player.status['revive_time'] = 86400

            case 'LETTING GO':
                os.remove(os.path.expanduser(f'~\\Documents\\pokeTamago\\save\\{player.properties["name"]}.json'))
                self.run = False
                os.execl(sys.executable, sys.executable, *sys.argv)

        if player.status["revive"]:
            deathWindow['death_frame'].update(visible=False)
            deathWindow['revive_frame'].update(visible=True)
            deathWindow['text1'].update(visible=False)
            deathWindow['text2'].update('Your pet is about to begin a new life.\n' +
            f'The process will take {f.time_counter(player.status["revive_time"])}.', visible=True)
            deathWindow['REVIVE'].update(visible=False)
            deathWindow['LETTING GO'].update(visible=False)
            deathWindow['MENU'].update(visible=True)

            if player.status['revive'] and player.status['revive_time'] == 0:
                deathWindow['death_frame'].update(visible=True)
                deathWindow['revive_frame'].update(visible=False)
                deathWindow['text1'].update(visible=True)
                deathWindow['text2'].update(visible=False)
                deathWindow['REVIVE'].update(visible=True)
                deathWindow['LETTING GO'].update(visible=True)
                deathWindow['MENU'].update(visible=False)

                player.condition['health'] = player.condition['MaxHP']
                player.condition['bored'] = 0
                player.condition['food'] = 100
                player.condition['exhausted'] = 0
                player.status['alive'] = True
                player.status['revive'] = False
                death = False
                break

    deathWindow.close()