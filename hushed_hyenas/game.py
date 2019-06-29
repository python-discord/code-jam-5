#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import json
import math

pygame.init()


class Game:

    def __init__(self):
        self.width = 1200
        self.height = 600
        self.bg_color = (255, 255, 255)  # Background color
        self.color = (0, 0, 0)
        self.window_menu = pygame.display.set_mode((int(self.width / 2), int(self.height / 2)))
        self.window = pygame.display.set_mode((self.width, self.height))
        self.caption = pygame.display.set_caption('Code jam')
        self.map = pygame.image.load(r'map_objects/earth2.png')

        # Resize image to fit in window
        self.map = pygame.transform.scale(
            self.map,
            (self.width, self.height)
        )

        self.clock = pygame.time.Clock()

        with open('countries.json') as json_data:
                self.data = json.load(json_data)

    def run(self):
        run = True
        window = self.window

        while run:
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

                current_distance=math.sqrt( (x - mouse_x)**2 + (y - mouse_y)**2 )

                if current_distance<closest_distance:
                    closest_distance = current_distance
                    closest_country = country

                pygame.draw.circle(window, (0, 0, 255), (int(x), int(y)), 3)

            if closest_country:
                print (closest_country['name'])
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                    pygame.quit()
                    quit()

                pygame.display.update()


game = Game()
game.run()
