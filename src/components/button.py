import PySimpleGUI as sg
from io import BytesIO
from PIL import Image

def button(self,text,size,disabled=False,tooltip=None):
    match self.settings['theme']:

        case "TamagoDefault":
            image = Image.open('src\\assets\\img\\buttons\\default_button.png')
            width, height = image.size
            resized_image = image.resize((int(width*size), int(height*size)))

            with BytesIO() as output:
                resized_image.save(output, format='PNG')
                data = output.getvalue()

            color = '#64778d'

        case "TamagoDark":
            image = Image.open('src\\assets\\img\\buttons\\dark_button.png')
            width, height = image.size
            resized_image = image.resize((int(width*size), int(height*size)))

            with BytesIO() as output:
                resized_image.save(output, format='PNG')
                data = output.getvalue()

            color = '#202124'

        case "TamagoLight":
            image = Image.open('src\\assets\\img\\buttons\\light_button.png')
            width, height = image.size
            resized_image = image.resize((int(width*size), int(height*size)))

            with BytesIO() as output:
                resized_image.save(output, format='PNG')
                data = output.getvalue()

            color = '#efefde'

    match disabled:

        case True:
            disabled = sg.BUTTON_DISABLED_MEANS_IGNORE

            image = Image.open('src\\assets\\img\\buttons\\disabled_button.png')
            width, height = image.size
            resized_image = image.resize((int(width*size), int(height*size)))

            with BytesIO() as output:
                resized_image.save(output, format='PNG')
                data = output.getvalue()

        case False:
            disabled = False

    return [sg.Button(text, image_source=data, mouseover_colors=('#41434D',color), border_width=0, 
        button_color=color, disabled=disabled, disabled_button_color=('#41434D', color), 
        tooltip=tooltip, k=text.upper())]