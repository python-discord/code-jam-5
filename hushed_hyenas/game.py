#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import json
import math
import os
from game_menu import main_menu

# Initializes pygame resources
pygame.init()

# Place the pygame window in the center of the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'


class Game:

    def __init__(self):
        self.width = 1200
        self.height = 600
        self.bg_color = (255, 255, 255)  # Background color
        self.window = pygame.display.set_mode((self.width, self.height))
        self.caption = pygame.display.set_caption('Code jam')
        self.original_map = pygame.image.load(r'map_objects/earth2large.png')
        self.clock = pygame.time.Clock()
        self.current_scene = 'Map'
        self.country = None
        self.font = pygame.font.Font(None, 25)

        # Resize image to fit in window
        self.map = pygame.transform.scale(self.original_map,
                                          (self.width, self.height))

        with open('countries.json') as json_data:
            self.data = json.load(json_data)

    def map_scene(self):
        window = self.window
        window.fill((202,236,252))
        
        if self.country is None:
            window.blit(self.map, (0, 0))

            closest_country = None
            closest_country_coords = None

            # Maximum value between cursor and country is 30
            closest_distance = 30

            mouse_x, mouse_y = pygame.mouse.get_pos()

            for country in self.data:

                lat, lon = country['latlng']

                x = int((180 + lon) / 360 * self.width)
                y = int((90 + lat * -1) / 180 * self.height)

                current_distance = math.sqrt((x - mouse_x) ** 2 +
                                             (y - mouse_y) ** 2)

                if current_distance < closest_distance:
                    closest_distance = current_distance
                    closest_country = country
                    closest_country_coords = x, y

                pygame.draw.circle(window, (0, 0, 255), (x, y), 3)

            # Checking if a country in the range of 30 units is found
            if closest_country is None:
                # Drawing the circle off-screen
                closest_country_coords = (-10, -10)

                # Displaying "Select a country" in the bottom right corner box
                closest_country = {'name': 'Select a country'}

            pygame.draw.circle(window, (255, 0, 0), closest_country_coords, 5)
            pygame.draw.rect(window, (0, 0, 0),
                             pygame.Rect(self.width - 300, self.height - 50, self.width,
                                         self.height))
            text = self.font.render(closest_country["name"], True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.width - 150, self.height - 25))
            window.blit(text, text_rect)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if closest_country is not None:
                        self.country = closest_country
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # If ESC is pressed during the game the menu is opened
                        main_menu(self.width, self.height, Game().run,
                                  Game().call_menu)

            self.zoom_map_width = self.width
            self.zoom_map_height = self.height

            self.blitx = 0
            self.blity = 0
            self.zoom = 0
        else:
            # Zoom into country when clicked

            self.zoom_map = pygame.transform.scale(self.original_map,
                                                   (int(self.zoom_map_width),
                                                    int(self.zoom_map_height)))
            lat, lon = self.country['latlng']

            x = (180 + lon) / 360 * self.zoom_map_width - self.width / 2
            y = (90 + lat * -1) / 180 * self.zoom_map_height \
                - self.height / 2
            self.zoom += 1

            self.blitx += (x - self.blitx) / (200 / self.zoom)
            self.blity += (y - self.blity) / (200 / self.zoom)

            window.blit(self.zoom_map, (self.blitx * -1, self.blity
                                        * -1))

            self.zoom_map_width = self.zoom_map_width * 1.01
            self.zoom_map_height = self.zoom_map_height * 1.01

            if self.zoom > 200:
                self.current_scene = 'Main'

    def main_scene(self):
        pass
        # window = self.window
        #
        # If this fill is enabled the screen goes white when the zoom finishes
        # window.fill(self.bg_color)
        #

    def run(self):
        # Game Loop
        while True:
            self.clock.tick(60)  # Set to 60 fps

            if self.current_scene == 'Map':
                self.map_scene()
            elif self.current_scene == 'Main':
                self.main_scene()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # If ESC is pressed during the game the menu is opened
                        game.call_menu()

            pygame.display.update()

    def call_menu(self):
        main_menu(self.width, self.height, Game().run, Game().call_menu)


# Game initializes with the menu being opened
game = Game()
game.call_menu()
