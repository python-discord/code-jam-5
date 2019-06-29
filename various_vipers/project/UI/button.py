"""Button model."""

import pygame as pg
from pygame import Rect

from project.constants import HEIGHT, WIDTH


def generate_buttons(btn_w: int, btn_h: int, btn_count: int, gap: int) -> list:
    """Generates new buttons of given parameters."""
    buttons = list()

    for i in range(btn_count):
        new_button = ButtonModel(
            btn_w=btn_w, btn_h=btn_h, btn_count=btn_count, pos=i + 1, gap=gap
        )

        buttons.append(new_button)
    return buttons


class ButtonModel:
    """Represents a button."""

    def __init__(self, btn_w: int, btn_h: int, btn_count: int, pos: int, gap: int):

        btn_area = btn_h * btn_count
        gap_area = (btn_count - 1) * gap

        self.margin_x = (WIDTH - btn_w) / 2
        self.margin_y = (HEIGHT - (btn_area + gap_area)) / 2

        self.left = self.margin_x
        self.top = self.margin_y + (gap * (pos - 1)) + (btn_h * (pos - 1))

        self.width = btn_w
        self.height = btn_h

        self.rect = Rect(self.left, self.top, self.width, self.height)

    def draw(self, screen: pg.Surface, hover: bool, image) -> None:
        """Draws the button on screen."""
        if not hover:
            screen.blit(image, self.rect)
        else:
            pass
