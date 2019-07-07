"""
Main Menu page.

Handling input and creating new events.
"""
import logging
import time
import webbrowser

import pygame as pg
from pygame.font import Font

from project.UI.element.button import Button, generate_main_buttons
from project.UI.fx.sound import Sound
from project.constants import (
    BUTTONS as BTN,
    ButtonProperties,
    Color,
    HEIGHT,
    REPO_LINK,
    WIDTH,
    WindowState,
)
from project.utils.helpers import load_img
from project.utils.helpers import realtime_to_ingame_delta_formatted
from project.utils.user_data import UserData

user_data = UserData()
user_data.load()


logger = logging.getLogger(__name__)


class MainMenu:
    """Represents Main Menu page."""

    def __init__(self, screen: pg.Surface):
        """Set initial main menu values."""
        self.screen = screen

        # load the main menu button images
        self.__load_images()

        # create buttons, store them and its states and extra github button
        self.__create_buttons()
        self.__store_buttons_and_states()  # the states are what the buttons do
        self.__load_set_github_button()

        # use last click timer for preventing too much clicking on the button
        self.last_click = int()
        self.font = Font(None, 40)

    def __load_images(self) -> None:
        """Loads all main menu button images and their hover states."""
        img_paths = [
            (BTN["play-btn"], BTN["play-btn-hover"]),
            (BTN["options-btn"], BTN["options-btn-hover"]),
            (BTN["credits-btn"], BTN["credits-btn-hover"]),
            (BTN["quit-btn"], BTN["quit-btn-hover"]),
        ]

        # load two types of images for the buttons
        # normal state and hover state
        self.images = [tuple([load_img(j) for j in i]) for i in img_paths]

    def draw(self, mouse_x: int, mouse_y: int, event) -> str:
        """Hadles all main menu events and draw every elements."""
        # assign the events with self for easy usage in other methods
        self.event = event
        self.mouse_x, self.mouse_y = mouse_x, mouse_y

        self.clicked = event.type == pg.MOUSEBUTTONDOWN
        # iterate all main menu buttons except the github icon
        for i, button in enumerate(self.buttons):
            # check if are hovered
            if button.rect.collidepoint(mouse_x, mouse_y):
                # draw button hover state
                button.draw(hover=True)

                if self.clicked:
                    # if the button is clicked - play the sound and
                    # return the state (the action) which the button does
                    Sound.click.play()
                    return self.states[i]
            else:
                # else draw its normal state
                button.draw()

        # draw the github button icon linking to our repo (bottom left)
        # and draw the highscore (bottom right)
        self.__draw_github_button()
        self.__draw_highscores()

        return WindowState.main_menu

    def __create_buttons(self) -> None:
        """
        Create main menu buttons on particular layout.

        Every main menu buttons centered and alligned with margin y on top and botoom
        """
        self.play_btn, self.opt_btn, self.credits_btn, self.quit_btn = generate_main_buttons(
            screen=self.screen,
            btn_w=ButtonProperties.main_btn_w,
            btn_h=ButtonProperties.main_btn_h,
            btn_count=4,
            gap=ButtonProperties.btn_gap,
            images=self.images,
        )

    def __store_buttons_and_states(self) -> None:
        """
        Create two lists for buttons and their acctions.

        So every button index coresponds to its action.

        The play button starts the game.
        The options button opens options page.
        The credits button opens credits page.
        The quit button quits the game.
        """
        self.buttons = [self.play_btn, self.opt_btn, self.credits_btn, self.quit_btn]
        self.states = [
            WindowState.game,
            WindowState.options,
            WindowState.credit,
            WindowState.quited,
        ]

    def __load_set_github_button(self) -> None:
        """
        Create the github icon button on the bottom right corner.

        This button links to our repository.
        """
        image = load_img(BTN["github"])
        image_hover = load_img(BTN["github-hover"])

        self.github_btn = Button(
            screen=self.screen,
            x=WIDTH - 120,
            y=HEIGHT - 120,
            width=100,
            height=100,
            image=image,
            image_hover=image_hover,
        )

    def __draw_github_button(self) -> None:
        """
        Draws the github icon button and its hover state.

        If it is clicked, it opens our repository in GitHub.
        """
        if self.github_btn.rect.collidepoint(self.mouse_x, self.mouse_y):
            self.github_btn.draw(hover=True)
            if self.clicked and (time.time() - self.last_click) > 0.3:
                Sound.click.play()
                self.last_click = time.time()
                webbrowser.open(REPO_LINK)
        else:
            self.github_btn.draw()

    def __draw_highscores(self) -> None:
        """Draws highscores in the bottom left."""
        date = realtime_to_ingame_delta_formatted(user_data.hiscore_modern)
        text = self.font.render(f"Highscore: {date}", True, Color.blue)

        self.screen.blit(text, (0, HEIGHT - text.get_height() - 10))
