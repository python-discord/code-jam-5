"""
Main Menu page.

Handling input and creating new events.
"""

import pygame as pg

from project.constants import Color, HEIGHT, WIDTH


class MainMenu:
    """Represents Main Menu page."""

    def __init__(self, screen):
        """Set initial main menu values."""
        self.screen = screen

        btn_w = 200
        btn_h = 100

        self.play_btn = self.options_btn = self.quit_button = pg.Rect(
            0, 0, btn_w, btn_h
        )

        self.h = HEIGHT
        self.gap = ((3 * 100) - WIDTH) / 3
        self.play_btn.midtop = (WIDTH / 2, 50)

    def handle_events(self, events: dict):
        """Hadle all main menu events."""
        pass

    def draw(self,):
        """Draw all main menu elements."""
        pg.draw.rect(self.screen, Color.white, self.play_btn)
