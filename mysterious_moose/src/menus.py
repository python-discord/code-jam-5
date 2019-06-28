import pygame
import logging

class MainMenu:
    def __init__(self):
        self.log = logging.getLogger("main.menu.MainMenu")
        self.log.setLevel(logging.INFO)

    def display(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.log.info("quit event received")
                return 0
        return -1
