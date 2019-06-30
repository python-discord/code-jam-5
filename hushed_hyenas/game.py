#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import json
import math
import os
import pygameMenu
from pygameMenu.locals import *

# Initializes pygame resources
pygame.init()

# Place the pygame window in the center of the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

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


class Game:

    def __init__(self):
        self.width = 1200
        self.height = 600
        self.bg_color = (255, 255, 255)  # Background color
        self.window_menu = pygame.display.set_mode((int(self.width / 2),
                                                    int(self.height / 2)))
        self.window = pygame.display.set_mode((self.width, self.height))
        self.caption = pygame.display.set_caption('Code jam')
        self.map = pygame.image.load(r'map_objects/earth2.png')
        self.menu_title = 'Game of the hyenas'
        self.clock = pygame.time.Clock()

        # Resize image to fit in window
        self.map = pygame.transform.scale(self.map, (self.width,
                                                     self.height))

        with open('countries.json') as json_data:
            self.data = json.load(json_data)

    def run(self):
        window = self.window

        menu.disable()

        # Game Loop
        while True:
            self.clock.tick(30)  # Set to 60 fps
            window.fill(self.bg_color)
            window.blit(self.map, (0, 0))

            closest_country = None
            closest_distance = self.width

            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]

            for country in self.data:

                lat = country['latlng'][0]
                lon = country['latlng'][1]

                x = (180 + lon) / 360 * self.width
                y = (90 + lat * -1) / 180 * self.height

                current_distance = math.sqrt(
                    (x - mouse_x) ** 2 + (y - mouse_y) ** 2)

                if current_distance < closest_distance:
                    closest_distance = current_distance
                    closest_country = country

                pygame.draw.circle(window, (0, 0, 255), (int(x),
                                   int(y)), 3)

            if closest_country:
                print(closest_country['name'])

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # If ESC is pressed during the game the menu is opened
                        menu.enable()

                        # Go to the menu loop
                        return

                pygame.display.update()

    def main_menu(self, *args):

        # Function to set the game background color when the menu is shown
        def main_menu_background():
            self.window.fill((40, 0, 40))

        # Main menu
        global menu
        menu = pygameMenu.Menu(self.window,
                               bgfun=main_menu_background,
                               font=pygameMenu.fonts.FONT_NEVIS,
                               menu_alpha=90,
                               menu_centered=True,
                               onclose=PYGAME_MENU_CLOSE,
                               title=self.menu_title,
                               title_offsety=5,
                               window_height=self.height,
                               window_width=self.width
                               )

        # About menu accessible from the main menu
        about_menu = pygameMenu.TextMenu(self.window,
                                         dopause=False,
                                         draw_text_region_x=50,
                                         font=pygameMenu.fonts.FONT_NEVIS,
                                         font_size_title=30,
                                         font_title=pygameMenu.fonts.FONT_8BIT,
                                         menu_color_title=(0, 40, 0),
                                         onclose=PYGAME_MENU_DISABLE_CLOSE,
                                         text_centered=True,
                                         text_fontsize=20,
                                         title='About',
                                         window_height=self.height,
                                         window_width=self.width
                                         )
        about_menu.add_option('Return to Menu', PYGAME_MENU_BACK)

        # Instructions menu accessible from the main menu
        instr_menu = pygameMenu.TextMenu(self.window,
                                         dopause=False,
                                         draw_text_region_x=50,
                                         font=pygameMenu.fonts.FONT_NEVIS,
                                         font_size_title=25,
                                         font_title=pygameMenu.fonts.FONT_8BIT,
                                         menu_color_title=(0, 40, 0),
                                         onclose=PYGAME_MENU_DISABLE_CLOSE,
                                         text_centered=True,
                                         text_fontsize=20,
                                         title='Instructions',
                                         window_height=self.height,
                                         window_width=self.width
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
        menu.add_option('Play', Game().run)
        menu.add_option(about_menu.get_title(), about_menu)
        menu.add_option(instr_menu.get_title(), instr_menu)
        menu.add_option('Exit', PYGAME_MENU_EXIT)

        # Main Menu Loop
        while True:

            self.clock.tick(20)

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


# Game initializes with the menu being opened
game = Game()
game.main_menu()
