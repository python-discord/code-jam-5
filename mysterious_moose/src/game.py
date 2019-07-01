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

        # whether the mouse is pressed
        self.pressed = False

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

        # gets mouse position
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)
        mouse_state = pygame.mouse.get_pressed()

        # background
        self.to_render.append([{"type": "bg", "colour": (0, 0, 0)}])

        if self.view == 0:
            # main view

            # static objects
            self.to_render.append([
                {
                    "type": "surface",
                    "surface": self.elements["mv.tray"],
                    "dest": self.elements["mv.tray.loc"]
                }
            ])

            buttons = (
                self.elements["mv.buttons.up"],
                self.elements["mv.buttons.down"],
                self.elements["mv.buttons.wm"]
            )

            up_arrow = self.elements["mv.up"]
            down_arrow = self.elements["mv.down"]
            wm_button = self.elements["mv.wm"]

            mouse_collision = mouse_pos.collidelist(buttons)

            if mouse_collision > -1:

                if mouse_state[0] == 1:
                    self.pressed = True
                    if mouse_collision == 0:
                        up_arrow = self.elements["mv.up.pressed"]
                    elif mouse_collision == 1:
                        down_arrow = self.elements["mv.down.pressed"]
                    elif mouse_collision == 2:
                        wm_button = self.elements["mv.wm.pressed"]

                elif mouse_state[0] == 0 and self.pressed is True:
                    self.pressed = False
                    if mouse_collision == 0:
                        pass
                    elif mouse_collision == 1:
                        pass
                    elif mouse_collision == 2:
                        self.view = 1

                else:
                    if mouse_collision == 0:
                        up_arrow = self.elements["mv.up.hover"]
                    elif mouse_collision == 1:
                        down_arrow = self.elements["mv.down.hover"]
                    elif mouse_collision == 2:
                        wm_button = self.elements["mv.wm.hover"]

            else:
                self.pressed = False

            self.to_render.append([
                {
                    "type": "surface",
                    "surface": up_arrow,
                    "dest": self.elements["mv.up.loc"]
                }, {
                    "type": "surface",
                    "surface": down_arrow,
                    "dest": self.elements["mv.down.loc"]
                }, {
                    "type": "surface",
                    "surface": wm_button,
                    "dest": self.elements["mv.wm.loc"]
                }

            ])

        elif self.view == 1:
            # world map
            buttons = (
                self.elements["wm.buttons.mv"],
            )

            mv_code = self.elements["wm.mv"]

            mouse_collision = mouse_pos.collidelist(buttons)

            if mouse_collision > -1:

                if mouse_state[0] == 1:
                    self.pressed = True
                    if mouse_collision == 0:
                        mv_code = self.elements["wm.mv.pressed"]

                elif mouse_state[0] == 0 and self.pressed is True:
                    self.pressed = False
                    if mouse_collision == 0:
                        self.view = 0

                else:
                    if mouse_collision == 0:
                        mv_code = self.elements["wm.mv.hover"]

            else:
                self.pressed = False

            self.to_render.append([
                {
                    "type": "surface",
                    "surface": mv_code,
                    "dest": self.elements["wm.mv.loc"]
                }
            ])

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
            "button_hover": (125, 125, 125),
            "button_pressed": (100, 100, 100),
            "tray": (50, 50, 50),
            "scroll": (75, 75, 75)
        }

        # viruses
        for virus in self.viruses:
            virus.graphic.update(resolution)

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

        button.blit(button_icon, button_centre)
        self.elements["mv.wm"] = button.copy()

        button.fill(colours["button_hover"])
        button.blit(button_icon, button_centre)
        self.elements["mv.wm.hover"] = button.copy()

        button.fill(colours["button_pressed"])
        button.blit(button_icon, button_centre)
        self.elements["mv.wm.pressed"] = button

        self.elements["mv.wm.loc"] = (0, 0)
        self.elements["mv.buttons.wm"] = button.get_rect()

        # virus tray
        virus_tray_width = resolution[0]//5
        virus_scroll_width = resolution[0]//40

        tray = pygame.Surface((virus_scroll_width + virus_tray_width, resolution[1]))

        scroll_bar = pygame.Rect(0, 0, virus_scroll_width, resolution[1])
        virus_select = pygame.Rect(virus_scroll_width, 0, virus_tray_width, resolution[1])

        pygame.draw.rect(tray, colours["scroll"], scroll_bar)
        pygame.draw.rect(tray, colours["tray"], virus_select)

        self.elements["mv.tray"] = tray
        self.elements["mv.tray.loc"] = (resolution[0] - virus_tray_width - virus_scroll_width, 0)

        # up scroll arrow
        top_scroll_arrow = pygame.Surface((virus_scroll_width, virus_scroll_width))

        top_scroll_arrow.fill(colours["button"])
        self.elements["mv.up"] = top_scroll_arrow.copy()
        top_scroll_arrow.fill(colours["button_hover"])
        self.elements["mv.up.hover"] = top_scroll_arrow.copy()
        top_scroll_arrow.fill(colours["button_pressed"])
        self.elements["mv.up.pressed"] = top_scroll_arrow
        self.elements["mv.up.loc"] = (
            resolution[0] - virus_tray_width - virus_scroll_width,
            0
        )
        self.elements["mv.buttons.up"] = pygame.Rect(
            self.elements["mv.up.loc"],
            (virus_scroll_width, virus_scroll_width)
        )

        # down scroll arrow
        bottom_scroll_arrow = pygame.Surface((virus_scroll_width, virus_scroll_width))

        bottom_scroll_arrow.fill(colours["button"])
        self.elements["mv.down"] = bottom_scroll_arrow.copy()
        bottom_scroll_arrow.fill(colours["button_hover"])
        self.elements["mv.down.hover"] = bottom_scroll_arrow.copy()
        bottom_scroll_arrow.fill(colours["button_pressed"])
        self.elements["mv.down.pressed"] = bottom_scroll_arrow
        self.elements["mv.down.loc"] = (
            resolution[0] - virus_tray_width - virus_scroll_width,
            resolution[1] - virus_scroll_width
        )
        self.elements["mv.buttons.down"] = pygame.Rect(
            self.elements["mv.down.loc"],
            (virus_scroll_width, virus_scroll_width)
        )

        # world view

        # button to main view
        # button width
        button_width = (resolution[0] // 15)
        button = pygame.Surface((button_width, resolution[1]))
        button.fill(colours["button"])

        button_icon = self.graphics.images["right arrow"]
        button_icon = pygame.transform.scale(button_icon, (button_width, button_width))

        # find button centre
        button_centre = button_icon.get_rect(
            center=(button.get_width() // 2, button.get_height() // 2))

        button.blit(button_icon, button_centre)
        self.elements["wm.mv"] = button.copy()

        button.fill(colours["button_hover"])
        button.blit(button_icon, button_centre)
        self.elements["wm.mv.hover"] = button.copy()

        button.fill(colours["button_pressed"])
        button.blit(button_icon, button_centre)
        self.elements["wm.mv.pressed"] = button

        self.elements["wm.mv.loc"] = (resolution[0] - button_width, 0)
        self.elements["wm.buttons.mv"] = pygame.Rect(
            self.elements["wm.mv.loc"],
            (button_width, resolution[1])
        )
