#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import json
import math
import os
from game_menu import main_menu
from gameobjects import Boxes
from news_list import get_level_1_news, get_level_2_news, get_level_3_news, \
    get_level_4_news, get_level_5_news
from random import randint

# Initializes pygame resources
pygame.init()

# Place the pygame window in the center of the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Instantiate the get_constants as constants
news_1 = get_level_1_news()
news_2 = get_level_2_news()
news_3 = get_level_3_news()
news_4 = get_level_4_news()
news_5 = get_level_5_news()

# Instantiate the News class for better usage
boxes = Boxes()

#   name , max_latitude , min_latitude , max_longitude , min_longitude
zoom_list = [['Russian', 81.86, 41.19, 27.9, -170], ['Canada', 83.21, 41.71, -52.62, -141.0],
             ['China', 53.56, 18.16, 134.78, 73.56], ['United States', 71.39, 5.87, -66.9, -180.0],
             ['Brazil', 5.26, -33.74, -29.3, -73.99], ['Australia', -9.23, -54.76, 159.11, 112.91],
             ['India', 35.99, 6.75, 97.4, 68.17], ['Argentina', -21.78, -55.05, -53.59, -73.58],
             ['Kazakhstan', 55.43, 40.55, 87.31, 46.49], ['Algeria', 37.09, 18.96, 12.0, -8.67],
             ['Congo, Dem. Rep.', 3.7, -5.03, 18.65, 11.21],
             ['Greenland', 83.64, 59.61, -11.41, -73.1]]


class Game:

    def __init__(self):
        self.width = 1200
        self.height = 600
        self.bg_color = (255, 255, 255)  # Background color
        self.window = pygame.display.set_mode((self.width, self.height))
        self.caption = pygame.display.set_caption('Code jam')
        self.original_map = pygame.image.load(r'map_objects/earth_large.png')
        self.icon_normal = pygame.image.load(r'map_objects/pin_default.png')
        self.icon_hover = pygame.image.load(r'map_objects/pin_hover.png')
        self.clock = pygame.time.Clock()
        self.current_scene = 'Map'
        self.country = None
        self.font = pygame.font.Font(None, 25)
        self.turn_number = '1'

        # this checker is used for debugging purposes of the different levels of colors for news
        self.checker = 0

        self.news1 = news_1['news1']
        self.news1_color = (225, 225, 225, 160)
        self.news2 = news_2['news1']
        self.news2_color = (135, 206, 250, 160)
        self.news3 = news_3['news1']
        self.news3_color = (144, 238, 144, 160)
        self.news4 = news_4['news1']
        self.news4_color = (255, 69, 0, 160)
        self.news5 = news_5['news1']
        self.news5_color = (255, 0, 0, 160)

        # Resize image to fit in window
        self.map = pygame.transform.scale(self.original_map, (self.width, self.height))

        with open('countries.json') as json_data:
            self.data = json.load(json_data)

    def map_scene(self):
        window = self.window
        window.fill((202, 236, 252))

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

                current_distance = math.sqrt((x - mouse_x) ** 2 + (y - mouse_y) ** 2)

                if current_distance < closest_distance:
                    closest_distance = current_distance
                    closest_country = country
                    closest_country_coords = x, y
                    closest_country_coords_hover = x - 9, y - 15

                # The -7 and -13 values are used to correct the pin image size to put
                # the bottom of the pin to the x and y point
                window.blit(self.icon_normal, (x - 7, y - 13))

            # Checking if a country in the range of 30 units is found
            if closest_country is None:
                # Drawing the pin off-screen
                closest_country_coords = closest_country_coords_hover = (-20, -20)

                # Displaying "Select a country" in the bottom right corner box
                closest_country = {'name': 'Select a country'}

            window.blit(self.icon_hover, closest_country_coords_hover)
            pygame.draw.rect(window, (0, 0, 0),
                             pygame.Rect(self.width - 300, self.height - 50, self.width,
                                         self.height))
            text = self.font.render(closest_country["name"], True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.width - 150, self.height - 25))
            window.blit(text, text_rect)

            # conditional to test the news levels
            # This is to be removed once the player's decisions impact the news
            if self.checker == 1:
                boxes.news_box(window, self.width, self.news1, self.news1_color)
            elif self.checker == 2:
                boxes.news_box(window, self.width, self.news2, self.news2_color)
            elif self.checker == 3:
                boxes.news_box(window, self.width, self.news3, self.news3_color)
            elif self.checker == 4:
                boxes.news_box(window, self.width, self.news4, self.news4_color)
            else:
                boxes.news_box(window, self.width, self.news5, self.news5_color)

            # Generate lists and strings to test the social and environmental boxes
            social_list = ['index a %', 'index b %', 'index c %', 'index d %', 'index b %',
                           'index c %', 'index d %']
            social_index = '\n'.join(str(e) for e in social_list)
            boxes.social_indexes(window, self.height, social_index)

            environmental_list = ['index e %', 'index f %', 'index g %', 'index h %', 'index b %',
                                  'index c %', 'index d %']
            environmental_index = '\n'.join(str(e) for e in environmental_list)
            boxes.environmental_indexes(window, self.height, environmental_index)

            boxes.turn_number(window, self.width, self.turn_number)
            boxes.game_status(window, self.width, 'values')

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if closest_country_coords is not (-20, -20):
                        self.country = closest_country
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    # Once the news are changed by the actions of the player we can remove this
                    news1_index = randint(1, 21)
                    self.news1 = news_1['news' + str(news1_index)]
                    news_index = randint(1, 2)
                    self.news2 = news_2['news' + str(news_index)]  # Get random news2
                    self.news3 = news_3['news' + str(news_index)]  # Get random news3

                    # rand to change the value of the checker each time the mouse button is clicked
                    # checker = 1 means news level 1 being shown
                    # checker = 2 means news level 2 being shown
                    # checker = 3 means news level 3 being shown
                    random = randint(0, 6)
                    if random == 0:
                        self.checker = 1
                    elif random == 1:
                        self.checker = 2
                    elif random == 2:
                        self.checker = 3
                    elif random == 3:
                        self.checker = 4
                    else:
                        self.checker = 5

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # If ESC is pressed during the world map state the menu is opened
                        game.call_menu()

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
                self.start_scene = True

    def main_scene(self):
        window = self.window

        # conditional to test the news levels
        # This is to be removed once the player's decisions impact the new
        # Only render when scene has started
        if self.start_scene:
            if self.checker == 1:
                boxes.news_box(window, self.width, self.news1, self.news1_color)
            elif self.checker == 2:
                boxes.news_box(window, self.width, self.news2, self.news2_color)
            elif self.checker == 3:
                boxes.news_box(window, self.width, self.news3, self.news3_color)
            elif self.checker == 4:
                boxes.news_box(window, self.width, self.news4, self.news4_color)
            else:
                boxes.news_box(window, self.width, self.news5, self.news5_color)

            # Generate lists and strings to test the social and environmental boxes
            social_list = ['index a %', 'index b %', 'index c %', 'index d %', 'index b %',
                           'index c %', 'index d %']
            social_index = '\n'.join(str(e) for e in social_list)
            boxes.social_indexes(window, self.height, social_index)

            environmental_list = ['index e %', 'index f %', 'index g %', 'index h %', 'index b %',
                                  'index c %', 'index d %']
            environmental_index = '\n'.join(str(e) for e in environmental_list)
            boxes.environmental_indexes(window, self.height, environmental_index)

            boxes.turn_number(window, self.width, '5')
            self.start_scene = False

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:

                # Once the news are changed by the actions of the player we can remove this block
                news1_index = randint(1, 21)
                self.news1 = news_1['news' + str(news1_index)]  # Get random news1 from the 21
                news_index = randint(1, 2)
                self.news2 = news_2['news' + str(news_index)]  # Get random news2 from the 2 news
                self.news3 = news_3['news' + str(news_index)]  # Get random news3 from the 2 news

                # rand to change the value of the checker each time the mouse button is clicked
                # checker = 1 means news level 1 being shown
                # checker = 2 means news level 2 being shown
                # checker = 3 means news level 3 being shown
                random = randint(0, 2)
                if random == 0:
                    self.checker = 1
                elif random == 1:
                    self.checker = 2
                else:
                    self.checker = 3

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.country = None
                    self.current_scene = 'Map'
                    game.run()

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
                        # If ESC is pressed during the zoom state the world map is opened
                        self.country = None
                        self.current_scene = 'Map'
                        game.run()

            pygame.display.update()

    def call_menu(self):
        main_menu(self.width, self.height, Game().run, Game().call_menu)


# Game initializes with the menu being opened
game = Game()
game.call_menu()
