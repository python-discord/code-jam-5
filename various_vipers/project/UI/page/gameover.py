"""
GameOver page.

Handling input and making changes.
"""
import logging

import pygame as pg

from project.UI.element.button import Button
from project.UI.fx.sound import Sound
from project.constants import (
    BUTTONS as BTN,
    ButtonProperties,
    Color,
    GOLD_COIN,
    HEIGHT,
    PATH_GAMEOVER_BG,
    STAR,
    WIDTH,
    WindowState,
)
from project.gameplay.game_state import GameState
from project.gameplay.period import Period
from project.utils.helpers import realtime_to_ingame_delta_formatted


logger = logging.getLogger(__name__)
game_vars = GameState()


class GameOver:
    """Represents GameOver page."""

    def __init__(self, screen: pg.Surface):
        self.screen = screen
        home_btn_img = pg.image.load(str(BTN["main-menu-btn"])).convert_alpha()
        home_btn_img_h = pg.image.load(str(BTN["main-menu-btn-hover"])).convert_alpha()

        self.background = pg.image.load(str(PATH_GAMEOVER_BG)).convert_alpha()

        self.star = pg.image.load(str(STAR)).convert_alpha()
        self.star = pg.transform.scale(self.star, (40, 40))
        self.gold_coin = pg.image.load(str(GOLD_COIN)).convert_alpha()
        self.gold_coin = pg.transform.scale(self.gold_coin, (40, 40))

        self.bg_rect_1 = pg.Rect(0, 0, WIDTH, HEIGHT)
        self.bg_rect_2 = pg.Rect(-WIDTH, 0, WIDTH, HEIGHT)

        self.home_btn = Button(
            screen=self.screen,
            x=ButtonProperties.back_btn_x,
            y=ButtonProperties.back_btn_y,
            width=ButtonProperties.back_btn_w,
            height=ButtonProperties.back_btn_h,
            image=home_btn_img,
            image_hover=home_btn_img_h,
        )

    def draw(self, mouse_x: int, mouse_y: int, event, period: Period):
        """Hadle all options events and draw elements."""
        self.__draw_infinity_bg()
        self.__draw_text_(period)

        if self.home_btn.rect.collidepoint(mouse_x, mouse_y):
            self.home_btn.draw(hover=True)

            if event.type == pg.MOUSEBUTTONDOWN:
                Sound.click.play()
                game_vars.reset_game = True
        else:
            self.home_btn.draw()
        return WindowState.gameover

    def __draw_infinity_bg(self):
        self.bg_rect_1.left += 1
        self.bg_rect_2.left += 1

        if self.bg_rect_1.left == WIDTH:
            self.bg_rect_1.left = -WIDTH
        if self.bg_rect_2.left == WIDTH:
            self.bg_rect_2.left = -WIDTH

        self.screen.blit(self.background, self.bg_rect_1)
        self.screen.blit(self.background, self.bg_rect_2)

    def __draw_text_(self, period: Period):
        font = pg.font.Font(None, 100)
        font2 = pg.font.Font(None, 50)
        font3 = pg.font.Font(None, 60)
        color = Color.black

        text_title = "GAME OVER !"
        text_subtitle = "NEW HISCORE !" if period.elapsed > period.hiscore else ""
        text_current_elapsed = realtime_to_ingame_delta_formatted(period.elapsed)
        text_best_elapsed = realtime_to_ingame_delta_formatted(
            max(period.hiscore, period.elapsed)
        )

        current_image = self.star if period.elapsed >= period.hiscore else None
        best_image = self.star if period.elapsed >= period.hiscore else self.gold_coin

        # (offset, surface, surface)
        # Offset is pixels down from previous surface
        # 1st surface is additional surface before text (optional)
        # 2nd surface is text
        lines = [
            (0, None, font.render(text_title, True, color)),
            (100, None, font2.render(text_subtitle, True, color)),
            (40, current_image, font3.render(text_current_elapsed, True, color)),
            (50, best_image, font3.render(text_best_elapsed, True, color)),
        ]

        current_offset = 0
        for offset, pre_image, text in lines:
            current_offset += offset
            x2 = int(WIDTH // 2) - int(text.get_width() // 2)
            y2 = int(HEIGHT // 3) + current_offset

            if pre_image is not None:
                x1 = x2 - pre_image.get_width() - 5
                y1 = (
                    y2
                    + int(text.get_height() // 2)
                    - int(pre_image.get_height() // 2)
                    - 5
                )
                self.screen.blit(pre_image, (x1, y1))
            self.screen.blit(text, (x2, y2))
