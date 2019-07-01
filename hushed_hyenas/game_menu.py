import thorpy


def main_menu(width, height, func_run, func_menu):

    def func_about():
        about_text = thorpy.make_text('Game of the Hyenas \n '
                                      'by \n\n '
                                      'AnDreWerDnA'
                                      ' \n 700y \n Pk \n\n '
                                      '-  Python Code Jam 5 -',
                                      25)

        normal_about, hover_about = 'assets/back-on.png',\
                                    'assets/back-off.png',

        back_button = thorpy.make_image_button(img_normal=normal_about,
                                               img_hover=hover_about,
                                               colorkey=(0, 0, 0))
        back_button.user_func = func_menu
        about_background = thorpy.Background(image='map_objects/menu_bg.jpg',
                                             elements=[about_text,
                                                       back_button])
        thorpy.store(about_background)
        about_menu = thorpy.Menu(about_background)
        about_menu.play()

    application = thorpy.Application((width, height), "Code Jam")

    # Different buttons for normal and hover
    normal, hover = 'assets/play-on.png', 'assets/play-off.png'
    normal_quit, hover_quit = 'assets/quit-on.png', 'assets/quit-off.png'
    normal_about, hover_about = 'assets/about-on.png', 'assets/about-off.png'

    play_button = thorpy.make_image_button(img_normal=normal,
                                           img_hover=hover,
                                           colorkey=(0, 0, 0))

    about_button = thorpy.make_image_button(img_normal=normal_about,
                                            img_hover=hover_about,
                                            colorkey=(0, 0, 0))

    quit_button = thorpy.make_image_button(img_normal=normal_quit,
                                           img_hover=hover_quit,
                                           colorkey=(0, 0, 0))

    background = thorpy.Background(image='map_objects/menu_bg.jpg',
                                   elements=[play_button,
                                             about_button,
                                             quit_button])
    # Set functions for the buttons
    play_button.user_func = func_run
    quit_button.set_as_exiter()
    about_button.user_func = func_about
    thorpy.store(background)
    menu = thorpy.Menu(background)
    menu.play()

    application.quit()
