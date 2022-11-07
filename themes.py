import PySimpleGUI as sg

sg.LOOK_AND_FEEL_TABLE['TamagoDefault'] = {'BACKGROUND': '#64778d',
                                           'TEXT': '#ebebeb',
                                           'INPUT': '#dddddd',
                                           'TEXT_INPUT': '#000000',
                                           'SCROLL': '#ebebeb',
                                           'BUTTON': ('#ebebeb', '#283b5b'),
                                           'PROGRESS': ('#283b5b', '#ebebeb'),
                                           'BORDER': 1,
                                           'SLIDER_DEPTH': 1,
                                           'PROGRESS_DEPTH': 0}

sg.LOOK_AND_FEEL_TABLE['TamagoDark'] = {'BACKGROUND': '#202124',
                                        'TEXT': '#f0f0f0',
                                        'INPUT': '#303134',
                                        'TEXT_INPUT': '#f0f0f0',
                                        'SCROLL': '#303134',
                                        'BUTTON': ('#f0f0f0', '#303134'),
                                        'PROGRESS': ('#202124', '#f0f0f0'),
                                        'SLIDER': '#303134',
                                        'BORDER': 1,
                                        'SLIDER_DEPTH': 1,
                                        'PROGRESS_DEPTH': 0}

sg.LOOK_AND_FEEL_TABLE['TamagoLight'] = {'BACKGROUND': '#efefde',
                                         'TEXT': '#000000',
                                         'INPUT': '#ffffff',
                                         'TEXT_INPUT': '#000000',
                                         'SCROLL': '#ffffff',
                                         'BUTTON': ('#000000', '#f7f7ef'),
                                         'PROGRESS': ('#0052e7', '#ffffff'),
                                         'BORDER': 1,
                                         'SLIDER_DEPTH': 1,
                                         'PROGRESS_DEPTH': 0}