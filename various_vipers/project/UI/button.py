"""Button model."""

import pygame as pg
from pygame import Rect

from project.constants import HEIGHT, WIDTH


def generate_main_buttons(btn_w: int, btn_h: int, btn_count: int, gap: int) -> list:
    """Generates new buttons of given parameters."""
    buttons = list()

    for i in range(btn_count):
        pos = i + 1

        btn_area = btn_h * btn_count
        gap_area = (btn_count - 1) * gap

        margin_x = (WIDTH - btn_w) / 2
        margin_y = (HEIGHT - (btn_area + gap_area)) / 2

        left = margin_x
        top = margin_y + (gap * (pos - 1)) + (btn_h * (pos - 1))

        new_button = ButtonModel(x=left, y=top, width=btn_w, height=btn_h)

        buttons.append(new_button)
    return buttons


class ButtonModel:
    """Represents a button."""

    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)

    def draw(self, screen: pg.Surface, image) -> None:
        """Draws the button on screen."""
        screen.blit(image, self.rect)
