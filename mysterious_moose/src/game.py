import logging

import pygame
import src.blocks as blocks
import src.world as world

log = logging.getLogger("main.game")
log.setLevel(logging.INFO)
log.info("game logger initialised")


class Game:
    def __init__(self, graphics):
        self.graphics = graphics
        self.blocks = blocks.get_blocks()
        self.world = world.World()
        self.view = 0  # current graphical view
        self.selected = -1  # currently selected virus
        self.viruses = []
        self.to_render = []

        # list of graphical elements
        self.elements = {}

        # get resolution
        display_info = pygame.display.Info()
        # initialise scalable elements
        self.resolution_change((display_info.current_w, display_info.current_h))

    def update(self):
        """ called each loop to update the game """
        # logic

        # graphics & mouse interactions
        # resets things to be rendered
        self.to_render = []
        if self.view == 0:
            # main view

            # button to world map
            self.to_render.append([
                {
                    "type": "surface",
                    "surface": self.elements["mv.wm"],
                    "dest": self.elements["mv.wm.loc"]},
                {
                    "type": "surface",
                    "surface": self.elements["mv.tray"],
                    "dest": self.elements["mv.tray.loc"]
                }
            ])

        elif self.view == 1:
            # world map
            pass
        elif self.view == 2:
            # market
            pass
        elif self.view == 3:
            # virus info
            pass
        elif self.view == 4:
            # virus creation
            pass
        else:
            log.error("view was set to an invalid value resetting")
            self.view = 0

        self.graphics.update(self.to_render)

    def resolution_change(self, resolution):
        """ updates graphical game elements for a new resolution """
        """ 
        abbreviation used in `elements`:
        mv: main view
        wm: world map
        mp: market
        vi: virus info
        vc: virus creation
        """
        # colours
        colours = {
            "button": (150, 150, 150),
            "tray": (50, 50, 50),
            "scroll": (75, 75, 75)
        }

        # main view

        # button to world map
        # button width
        button_width = (resolution[0]//15)
        button = pygame.Surface((button_width, resolution[1]))
        button.fill(colours["button"])

        button_icon = self.graphics.images["world icon"]
        button_icon = pygame.transform.scale(button_icon, (button_width, button_width))

        # find button centre
        button_centre = button_icon.get_rect(center=(button.get_width()//2, button.get_height()//2))

        # draw button icon onto the button
        button.blit(button_icon, button_centre)

        self.elements["mv.wm"] = button
        self.elements["mv.wm.loc"] = (0, 0)
        self.elements["mv.buttons.wm.rect"] = button.get_rect()

        # virus tray
        virus_tray_width = resolution[0]//5
        virus_scroll_width = resolution[0]//40

        tray = pygame.Surface((virus_scroll_width + virus_tray_width, resolution[1]))

        scroll_bar = pygame.Rect(0, 0, virus_scroll_width, resolution[1])
        virus_select = pygame.Rect(virus_scroll_width, 0, virus_tray_width, resolution[1])

        top_scroll_arrow = pygame.Rect(
            0, 0,
            virus_scroll_width, virus_scroll_width
        )
        bottom_scroll_arrow = pygame.Rect(
            0, resolution[1] - virus_scroll_width,
            virus_scroll_width, virus_scroll_width
        )

        pygame.draw.rect(tray, colours["scroll"], scroll_bar)
        pygame.draw.rect(tray, colours["tray"], virus_select)
        pygame.draw.rect(tray, colours["button"], top_scroll_arrow)
        pygame.draw.rect(tray, colours["button"], bottom_scroll_arrow)

        self.elements["mv.tray"] = tray
        self.elements["mv.tray.loc"] = (resolution[0] - virus_tray_width - virus_scroll_width, 0)
        self.elements["mv.buttons.up"] = top_scroll_arrow
        self.elements["mv.buttons.down"] = bottom_scroll_arrow
