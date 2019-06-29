import pygame
import logging


class MainMenu:
    def __init__(self, renderer):
        self.renderer = renderer
        self.log = logging.getLogger("main.menu.MainMenu")
        self.log.setLevel(logging.INFO)
        self.graphics = [[
            {"type": "bg", "colour": (255, 255, 255)}
        ],
            []  # list edited by self.resolution_change()
        ]
        self.resolution_change()

    def resolution_change(self):
        # get the display size
        resolution = pygame.display.get_surface()
        resolution = (resolution.get_width(), resolution.get_height())
        self.log.debug("resolution: " + str(resolution))

        # title
        title = self.renderer.fonts["main"].render(
            text="Anthropodemics",
            size=1000
        )
        title_size = title[1][2:]

        title = pygame.transform.scale(title[0], (
            resolution[0]//5*4,
            int(resolution[0]//5*4*title_size[1]/title_size[0])
        ))

        title_size = title.get_rect  # get the new title size after transformation

        # puts elements in graphics to be rendered
        self.graphics[1] = [
            {"type": "surface", "surface": title, "dest": (resolution[0]//10, 20)}
        ]

    def display(self, events):
        # make a copy of graphics for editing
        graphics = self.graphics

        for event in events:
            pass
        self.renderer.update(graphics)


class Options:
    def __init__(self, renderer):
        self.renderer = renderer
        self.log = logging.getLogger("main.menu.OptionMenu")
        self.log.setLevel(logging.INFO)
        self.graphics = [[
            {"type": "bg", "colour": (255, 5, 255)}
        ]]
        self.resolution_change()

    def resolution_change(self):
        # get the display size
        resolution = pygame.display.get_surface()
        resolution = (resolution.get_width(), resolution.get_height())
        self.log.debug("resolution: " + str(resolution))

    def display(self):
        pass
