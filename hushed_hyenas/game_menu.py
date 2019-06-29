import pygameMenu
from pygameMenu.locals import *
import pygame


def main_menu(window, width, height, title, *args):

    def main_menu_background():
        window.fill((40, 0, 40))

    menu = pygameMenu.Menu(window,
                           bgfun=main_menu_background,
                           font=pygameMenu.fonts.FONT_NEVIS,
                           menu_alpha=90,
                           menu_centered=True,
                           onclose=PYGAME_MENU_CLOSE,
                           title=title,
                           title_offsety=5,
                           window_height=height,
                           window_width=width
                           )
    menu.add_option('Play', PYGAME_MENU_BACK)
    menu.add_option('Exit', PYGAME_MENU_EXIT)

    run = True
    clock = pygame.time.Clock()
    while run:

        clock.tick(20)
        window.fill((255, 255, 255))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu.enable()

        menu.mainloop(events)
        pygame.display.flip()
