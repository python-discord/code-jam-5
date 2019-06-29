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
        self.intersects = dict()

        # button colours
        self.button_colour = (200, 100, 50)
        self.button_hover_colour = (100, 100, 50)
        self.button_click_colour = (100, 0, 50)

        # True if the mouse is currently pressed
        self.pressed = False

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
        # get the new title size after transformation
        title_rect = title.get_rect()
        title_size = (title_rect.width, title_rect.height)

        # menu buttons
        # play
        play_button = pygame.Rect(
            resolution[0]//5*2,
            title_size[1] + 40,
            resolution[0]//5,
            50
        )
        play_text = self.renderer.fonts["main"].render(
            text="Play",
            size=40
        )[0]
        play_text_pos = play_text.get_rect(center=(resolution[0]/2, title_size[1] + 65))

        # options
        options_button = pygame.Rect(
            resolution[0] // 5 * 2,
            title_size[1] + 100,
            resolution[0] // 5,
            50
        )
        options_text = self.renderer.fonts["main"].render(
            text="Options",
            size=40
        )[0]
        options_text_pos = options_text.get_rect(center=(resolution[0] / 2, title_size[1] + 125))

        # puts elements in graphics to be rendered
        self.graphics[1] = [
            {"type": "surface", "surface": title, "dest": (resolution[0]//10, 20)},
            {"type": "rect", "rect": play_button, "colour": self.button_colour},
            {"type": "surface", "surface": play_text, "dest": play_text_pos},
            {"type": "rect", "rect": options_button, "colour": self.button_colour},
            {"type": "surface", "surface": options_text, "dest": options_text_pos}
        ]

        # dict of intersects for the mouse
        self.intersects = {"play": play_button, "options": options_button}

    def display(self, events):
        # make a copy of graphics for editing
        graphics = self.graphics

        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)
        mouse_state = pygame.mouse.get_pressed()

        if mouse_pos.collidelist(list(self.intersects.values())):
            over = mouse_pos.collidedict(self.intersects)[0]
            if mouse_state[0] is True:
                self.pressed = True
                if over == "play":
                    self.graphics[1][1]["colour"] = self.button_click_colour
                elif over == "options":
                    self.graphics[1][1]["colour"] = self.button_click_colour
            elif mouse_state[0] is False and self.pressed is True:
                self.pressed = False
                if over == "play":
                    return 3
                elif over == "options":
                    return 2
            else:
                if over == "play":
                    self.graphics[1][1]["colour"] = self.button_hover_colour
                if over == "options":
                    self.graphics[1][1]["colour"] = self.button_hover_colour
        else:
            self.graphics[1][1]["colour"] = self.button_colour
            self.graphics[1][3]["colour"] = self.button_colour

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
