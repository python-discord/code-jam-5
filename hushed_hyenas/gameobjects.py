'''
File with objects used along the project, such as `Button`
'''

from time import sleep
import pygame
import thorpy
from tkinter import ttk
import tkinter as tk


def upgrade_menu():
    upgrade_window = tk.Tk()
    upgrade_window.geometry('400x400+0+0')
    upgrade_window.title("Upgrades window")

    # Example tkinter treeview widget use
    tree = ttk.Treeview(upgrade_window)
    tree["columns"] = ("one", "two")
    tree.column("one", width=150)
    tree.column("two", width=100)
    tree.heading("one", text="column A")
    tree.heading("two", text="column B")
    tree.insert("", 0, text="Line 1", values=("1A", "1b"))
    tree.insert("", "end", text="sub dir 2", values=("2A", "2B"))
    # insert sub-item, method 1
    id2 = tree.insert("", "end", "dir2", text="Dir 2")
    tree.insert(id2, "end", text="sub dir 2-1", values=("2A", "2B"))
    tree.insert(id2, "end", text="sub dir 2-2", values=("2A-2", "2B-2"))
    # insert sub-item, method 2
    tree.insert("", "end", "dir3", text="Dir 3")
    tree.insert("dir3", "end", text=" sub dir 3", values=("3A", "3B"))
    tree.pack()

    upgrade_window.mainloop()


class Boxes:
    def __init__(self):
        self.font = pygame.font.Font(None, 25)
        self.blue = (135, 206, 250, 190)
        self.gray = (225, 225, 225, 190)
        self.green = (144, 238, 144, 190)
        self.yellow = (250, 250, 40, 160)
        self.purple = (221, 160, 221, 160)
        self.black = (0, 0, 0, 170)
        self.white = (255, 255, 255)
        self.status_color = (42, 38, 38, 160)
        self.turn_main_color = (22, 21, 60, 160)

        # Distance used for better visual effect when placing objects
        self.distance_from_border = 4

    def news_box(self, window, screen_width: int, news: str, color: tuple):
        """
        Creates a news box object
        :param window - Surface it will be created on
        :param screen_width - Width of the surface
        :param news - Which news will be displayed
        :param color - Which  color will be used, based on the news level
        :return:
        """
        text = thorpy.MultilineText(news, (screen_width / 2, 70))
        box = thorpy.Box(elements=[text])
        box.surface = window
        box.set_topleft((screen_width / 4, self.distance_from_border))
        box.set_main_color(color)
        box.blit()
        box.update()

    def social_indexes(self, window, screen_height: int, index: str):
        """
        Creates the social object box
        :param window - Surface it wil be created on
        :param screen_height - Height of the surface
        :param index - Which index will be displayed
        :return:
        """
        text = thorpy.MultilineText(index, (75, screen_height / 4))
        title = thorpy.OneLineText('Social Indexes')
        box = thorpy.Box(elements=[title, text])
        box.surface = window
        box.set_topleft((self.distance_from_border, screen_height / 6))
        box.set_main_color(self.yellow)
        box.blit()
        box.update()

    def environmental_indexes(self, window, screen_height: int, index: str):
        """
        Creates the social object box
        :param window - Surface it wil be created on
        :param screen_height - Height of the surface
        :param index - Which index will be displayed
        :return:
        """
        text = thorpy.MultilineText(index, (75, screen_height / 4))
        title = thorpy.OneLineText('Environmental')
        box = thorpy.Box(elements=[title, text])
        box.surface = window
        box.set_topleft((self.distance_from_border, screen_height / 2))
        box.set_main_color(self.purple)
        box.blit()
        box.update()

    def game_status(self, window, screen_width: int):
        """
        Display the game status for the main indexes
        :param window - Surface it wil be created on
        :param screen_width - Width of the surface
        :return:
        """
        title = thorpy.OneLineText('Game Status')
        title.set_font_size(15)
        title.set_font_color(self.white)

        cfc = thorpy.Element("CFC: 8%")
        cfc.set_font_size(10)
        cfc.set_size((60, 25))

        sf9 = thorpy.Element("SF9: 9%")
        sf9.set_font_size(10)
        sf9.set_size((60, 25))

        methane = thorpy.Hoverable("Methane: 100%")
        methane.set_font_size(10)
        methane.set_size((100, 25))

        box = thorpy.Box(elements=[title, cfc, sf9, methane])
        box.surface = window
        box.set_topleft((screen_width - 220, self.distance_from_border))
        box.set_main_color(self.status_color)
        box.blit()
        box.update()

    def turn_number(self, window, screen_width: int, turn_number: int):
        """
        :param window - Surface it wil be created on
        :param screen_width - Width of the surface
        :param turn_number - Number of the turn the players is on
        :return:
        """
        title = thorpy.OneLineText('Turn')
        title.set_font_color(self.white)
        title.set_font_size(18)
        text = thorpy.OneLineText(str(turn_number))  # Turn number must be transformed to string
        text.set_font_size(30)
        text.set_font_color(self.white)
        box = thorpy.Box(elements=[title, text])
        box.surface = window
        box.set_topleft((screen_width - 53, self.distance_from_border))
        box.set_main_color(self.turn_main_color)
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
