import pygame
import logging


class MainMenu:
    def __init__(self, renderer):
        self.renderer = renderer
        self.log = logging.getLogger("main.menu.MainMenu")
        self.log.setLevel(logging.INFO)
        self.graphics = [[
            {"type": "bg", "colour": (255, 255, 255)}
        ]]
        self.resolution_change()

    def resolution_change(self):
        # get the display size
        resolution = pygame.display.get_surface()
        resolution = (resolution.get_width(), resolution.get_height())
        self.log.debug("resolution: " + str(resolution))

        # title
        title = self.renderer.fonts["main"].render(
            text="Anthropodemics",
            size=50
        )
        title_size = title
        self.log.debug("Title size: " + str(title_size))

    def display(self, events):
        # make a copy of graphics for editing
        graphics = self.graphics

        for event in events:
            pass
        self.renderer.update(graphics)


class Options:
    def __init__(self, renderer):
        self.renderer = renderer
        self.log = logging.getLogger("main.menu.MainMenu")
        self.log.setLevel(logging.INFO)
        self.graphics = [[
            {"type": "bg", "colour": (255, 255, 255)}
        ]]
        self.resolution_change()

    def resolution_change(self):
        # get the display size
        resolution = pygame.display.get_surface()
        resolution = (resolution.get_width(), resolution.get_height())
        self.log.debug("resolution: " + str(resolution))

    def display(self):
        pass
