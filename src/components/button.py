import src.hooks.funct as f
import PySimpleGUI as sg


def button(self,text,size,disabled=False,visible=True,return_key=False,pad=(0,0)):
    match self.settings['theme']:

        case "TamagoDefault":
            data = f.image2data(None,True,'buttons\\default_button', size)

            color = ((sg.theme_text_color(),sg.theme_background_color()))

        case "TamagoDark":
            data = f.image2data(None,True,'buttons\\dark_button', size)

            color = ((sg.theme_text_color(),sg.theme_background_color()))

        case "TamagoLight":
            data = f.image2data(None,True,'buttons\\light_button', size)

            color = (sg.theme_text_color(),sg.theme_background_color())

    match disabled:

        case True:
            disabled = sg.BUTTON_DISABLED_MEANS_IGNORE

            data = f.image2data(None,True,'buttons\\disabled_button', size)

            color = ('#363840',sg.theme_background_color())

        case False:
            disabled = False

    return sg.Button(text, image_source=data, border_width=0, pad=pad, mouseover_colors=color, 
        button_color=color, disabled=disabled, bind_return_key=return_key, visible=visible, 
        font=('',int(20*size),'normal'), k=text.upper())
