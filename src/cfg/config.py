import PySimpleGUI as sg
import json
import os


path = os.path.expanduser('~\\Documents\\pokeTamago\\cfg')

if os.path.exists(path):
    with open(f'{path}\\settings.json', 'r') as settings:
                    data = json.load(settings)
                    settings = data

    match settings['theme']:

        case "TamagoDefault":
            background = '#516073'
            titlebar = '#283b5b'

        case "TamagoDark":
            background = '#303134'
            titlebar = '#303134'

        case "TamagoLight":
            background = '#bfbfb2'
            titlebar = '#0052e7'

    scale = settings['scale']

else:
    background = None
    titlebar = None
    scale = 1

sg.set_options(
    icon='src\\assets\\img\\logo.ico',
    button_color=None,
    element_size=(100, 100),
    button_element_size=(8, 0),
    margins=(0, 0),
    element_padding = (None, None),
    auto_size_text = True,
    auto_size_buttons = True,
    font = ('Pokemon Pixel Font', 24, 'normal'),
    border_width = 1,
    slider_border_width = 1,
    slider_relief = sg.RELIEF_RAISED,
    slider_orientation = None,
    autoclose_time = 3,
    message_box_line_width = None,
    progress_meter_border_depth = None,
    progress_meter_style = None,
    progress_meter_relief = sg.RELIEF_RAISED,
    progress_meter_color = ('#28fc03','#f2f2f2'),
    progress_meter_size = None,
    text_justification = 'c',
    background_color = background,
    element_background_color = background,
    text_element_background_color = background,
    input_elements_background_color = 'white',
    input_text_color = 'black',
    scrollbar_color = 'gray',
    text_color = 'black',
    element_text_color='white',
    debug_win_size=(500, 300),
    window_location=(None, None),
    error_button_color=(None, None),
    tooltip_time=200,
    tooltip_font=('Pokemon Pixel Font', 24, 'normal'),
    use_ttk_buttons=False,
    ttk_theme='alt',
    suppress_error_popups=True,
    suppress_raise_key_errors=True,
    suppress_key_guessing = True,
    warn_button_key_duplicates = False,
    enable_treeview_869_patch = True,
    enable_mac_notitlebar_patch = False,
    use_custom_titlebar = True,
    titlebar_background_color = titlebar,
    titlebar_text_color = 'white',
    titlebar_font = ('', 10, 'normal'),
    titlebar_icon = 'src\\assets\\img\\icon.png',
    user_settings_path = None,
    pysimplegui_settings_path = None,
    pysimplegui_settings_filename = None,
    keep_on_top = True,
    dpi_awareness = True,
    scaling = scale,
    disable_modal_windows = False,
    force_modal_windows = True,
    tooltip_offset = (10, 10),
    sbar_trough_color = None,
    sbar_background_color = None,
    sbar_arrow_color = None,
    sbar_width = None,
    sbar_arrow_width = None,
    sbar_frame_color = None,
    sbar_relief = None,
    alpha_channel = 1
    )