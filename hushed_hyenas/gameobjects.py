'''
File with objects used along the project, such as `Button`
'''

from time import sleep

import pygame
import thorpy


class Boxes:
    def __init__(self):
        self.font = pygame.font.Font(None, 25)
        self.blue = (135, 206, 250, 160)
        self.gray = (225, 225, 225, 160)
        self.green = (144, 238, 144, 160)
        self.default_color = (230, 230, 230)

    def news_box(self, window, screen_width, news, color):
        text = thorpy.MultilineText(news, (screen_width / 2, 70))
        box = thorpy.Box(elements=[text])
        box.surface = window
        box.set_topleft((screen_width / 4, 0))
        box.set_main_color(color)
        box.blit()
        box.update()


class Button(pygame.sprite.Sprite):

    def __init__(self, pos: tuple, img: str):
        '''
        Creates new Button object

        param pos - Position of button
        type pos  - tuple

        param img - Name of image, must be without `_on.png` or `_off.png`
        type img  - str
        '''

        # Running `__init__` function of the parent class
        super().__init__()

        self.pos = pos

        # Load both phases of the button
        self.img_on = pygame.image.load(img + '_on.png')
        self.img_off = pygame.image.load(img + '_off.png')

        # Set current image of the button that should be displayed
        self.image = self.img_off

    def is_touching_mouse(self, mouse_pos: tuple) -> bool:
        '''
        Returns `True` if the mouse is on the button, else it returns `False`

        param mouse_pos - The position of the mouse
        type mouse_pos  - tuple
        '''
        mouse_pos_in_button = (mouse_pos[0] - self.pos[0], mouse_pos[1] - self.pos[1])
        return bool(self.current_img.get_rect().collidepoint(*mouse_pos_in_button))

    def draw(self, win: pygame.Surface) -> None:
        '''
        Draws the button

        param win - Surface the button should be drawn on
        type win  - pygame.Surface
        '''
        win.blit(self.current_img, self.pos)

    def click(self):
        '''
        Plays the click "animation"
        '''
        self.image = self.img_on
        sleep(0.25)
        self.image = self.img_off
        sleep(0.10)
