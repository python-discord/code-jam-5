import pygameMenu
from pygameMenu.locals import *
import pygame

about = ['Game of the Hyenas',
         'by',
         PYGAMEMENU_TEXT_NEWLINE,
         'AnDreWerDnA',
         '700y',
         'Pk',
         PYGAMEMENU_TEXT_NEWLINE,
         '  -   Python Code Jam 5 Project   -  ']

instructions = ['1) Fusce aliquam, nunc eu pretium accumsan',
                '2) Neque massa aliquam mauris, id consectetur',
                '3) Quisque lacinia mi ipsum, eget posuere elit',
                '4) Sed quis justo cursus ligula mattis tincidunt',
                '5) Morbi ut erat ultricies, lacinia dui in',
                '6) Nulla ut efficitur sem',
                '7) Phasellus sollicitudin nibh massa, ut pharetra',
                '8) Mauris ex nibh, malesuada id feugiat vitae']


def main_menu(window, width, height, font, title, game_function):
    # Function to set the game background color when the menu is shown
    def main_menu_background():
        window.fill((40, 0, 40))

    # Main menu
    global menu
    menu = pygameMenu.Menu(window,
                           bgfun=main_menu_background,
                           font=font,
                           menu_alpha=90,
                           menu_centered=True,
                           onclose=PYGAME_MENU_CLOSE,
                           title=title,
                           title_offsety=5,
                           window_height=height,
                           window_width=width
                           )

    # About menu accessible from the main menu
    about_menu = pygameMenu.TextMenu(window,
                                     dopause=False,
                                     draw_text_region_x=50,
                                     font=pygameMenu.fonts.FONT_NEVIS,
                                     font_size_title=30,
                                     font_title=pygameMenu.fonts.FONT_8BIT,
                                     menu_color_title=(12, 12, 200),
                                     onclose=PYGAME_MENU_DISABLE_CLOSE,
                                     text_centered=True,
                                     text_fontsize=20,
                                     title='About',
                                     window_height=height,
                                     window_width=width
                                     )
    about_menu.add_option('Return to Menu', PYGAME_MENU_BACK)

    # Instructions menu accessible from the main menu
    instr_menu = pygameMenu.TextMenu(window,
                                     dopause=False,
                                     draw_text_region_x=50,
                                     font=pygameMenu.fonts.FONT_NEVIS,
                                     font_size_title=25,
                                     font_title=pygameMenu.fonts.FONT_8BIT,
                                     menu_color_title=(0, 90, 0),
                                     onclose=PYGAME_MENU_DISABLE_CLOSE,
                                     text_centered=True,
                                     text_fontsize=20,
                                     title='Instructions',
                                     window_height=height,
                                     window_width=width
                                     )
    instr_menu.add_option('Return to Menu', PYGAME_MENU_BACK)

    # Add info from instructions list into the instructions menu lines
    for line in instructions:
        instr_menu.add_line(line)
    instr_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)

    # Add info from the about list into the about menu lines
    for line in about:
        about_menu.add_line(line)
    about_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)

    # Buttons
    menu.add_option('Play', game_function)
    menu.add_option(about_menu.get_title(), about_menu)
    menu.add_option(instr_menu.get_title(), instr_menu)
    menu.add_option('Exit', PYGAME_MENU_EXIT)

    # Main Menu Loop
    while True:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        menu.mainloop(events)

        pygame.display.flip()
