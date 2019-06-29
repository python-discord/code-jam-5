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


class Game:

    def __init__(self):
        self.width = 1200
        self.height = 600
        self.bg_color = (255, 255, 255)  # Background color
        self.color = (0, 0, 0)
        self.window_menu = pygame.display.set_mode((int(self.width / 2),
                                                    int(self.height / 2)))
        self.window = pygame.display.set_mode((self.width, self.height))
        self.caption = pygame.display.set_caption('Code jam')
        self.map = pygame.image.load(r'map_objects/earth2.png')
        self.menu_title = 'Game of the hyenas'

        # Resize image to fit in window

        self.map = pygame.transform.scale(self.map, (self.width,
                                                     self.height))

        self.clock = pygame.time.Clock()

        with open('countries.json') as json_data:
            self.data = json.load(json_data)

    def run(self):
        window = self.window

        menu.disable()

        # Game Loop
        while True:
            self.clock.tick(60)  # Set to 60 fps
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

        # Function to set the game background when the menu is shown
        def main_menu_background():
            self.window.fill((40, 0, 40))

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
        # Buttons
        menu.add_option('Play', Game().run)
        menu.add_option('Exit', PYGAME_MENU_EXIT)

        # Main Menu Loop
        while True:

            self.clock.tick(20)
            self.window.fill((255, 255, 255))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            menu.mainloop(events)

            pygame.display.flip()


# Game now initializes with the menu being opened
game = Game()
game.main_menu()
