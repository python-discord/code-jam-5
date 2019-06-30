# Some of this skeleton was stolen from the aliens pygame example
import pygame
from pygame.rect import Rect
from pygame.constants import KEYDOWN, K_ESCAPE, QUIT, K_SPACE
import media

if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")


class Button(pygame.sprite.Sprite):
    def __init__(self, button_text, click_sound):
        self.rect = self.image.get_rect()
        self.click_sound = click_sound

    def on_click(self):
        """I made this method up; figure out how we detect button clicks"""
        self.click_sound.play()
        # I'm just playing the beep as a test that it's working, it won't
        # be in the final version
        pass


class ButtonPanel:
    def __init__(self):
        pass
        # TODO put a button here, or multiple, depending on what we decide
        # we want the game to look like


class CC:  # TODO game name goes here
    """Class should hold information about state of game
    This includes current environment value and such.
    Sprites and such should probably be held at class-level or module-level
     instead? maybe? idk lol
    """
    def __init__(self):
        pygame.init()

        screenrect = Rect(0, 0, 640, 480)
        bestdepth = pygame.display.mode_ok(screenrect.size, 0, 32)
        pygame.display.set_mode(screenrect.size, 0, bestdepth)

        self.exit_requested = False
        self.score = 0
        self.button_panel = ButtonPanel()
        self.clock = pygame.time.Clock()

        self.images = media.load_images()
        self.sounds = media.load_sounds()

        self.environment_image = None  # images["environment_neutral"]
        # If we want to display the score, that shouldn't be too hard. If
        # we want to display the environment only instead, that works too.
        # TODO display environment_image in background
        # TODO add button panel to screen

    def update(self):
        """Called on new frame"""
        # TODO update score field, update environment image,
        # update anything we need to update in the button panel
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN
                                      and event.key == K_ESCAPE):
                self.exit_requested = True
                return

        keystate = pygame.key.get_pressed()
        if keystate[K_SPACE]:
            self.sounds["beep"].play()
            # Just for testing sounds
        self.clock.tick(40)
        # Or maybe don't? It's a clicker, so having an fps limit might be dumb

    def play(self):
        """Begins the game. Detect any exits and exit gracefully."""
        while not self.exit_requested:
            self.update()
        pygame.quit()


def main():
    game = CC()
    game.play()


if __name__ == "__main__":
    main()
