# Some of this skeleton was stolen from the aliens pygame example
import pygame
from pygame.rect import Rect
from pygame.constants import (
    KEYDOWN,
    K_ESCAPE,
    K_SPACE,
    MOUSEBUTTONDOWN,
    QUIT,
)
import media

if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")


class Crank(pygame.sprite.Sprite):
    """Hand Crank that rotates when clicks."""
    def __init__(self, crank_image, click_sound):
        pygame.sprite.Sprite.__init__(self)
        self.image = crank_image
        self.rect = self.image.get_rect()
        self.click_sound = click_sound
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.spinning = 0

    def update(self):
        "spin based on state"
        if self.spinning:
            self._spin()

    def _spin(self):
        "Spin the sprite one full revolution"
        center = self.rect.center
        self.spinning += 12
        if self.spinning >= 360:
            self.spinning = 0
            self.image = self.original
        else:
            self.image = pygame.transform.rotate(self.original, self.spinning)
            self.rect = self.image.get_rect(center=center)

    def clicked(self):
        "this will cause the crank to start spinning"
        if not self.spinning:
            self.click_sound.play()
            self.spinning = 1
            self.original = self.image


class ClimateClicker:
    """Class should hold information about state of game
    This includes current environment value and such.
    Sprites and such should probably be held at class-level or module-level
     instead? maybe? idk lol
    """
    def __init__(self):
        pygame.init()

        screenrect = Rect(0, 0, 640, 480)
        bestdepth = pygame.display.mode_ok(screenrect.size, 0, 32)
        self.screen = pygame.display.set_mode(screenrect.size, 0, bestdepth)
        pygame.display.set_caption('Climate Clicker')

        self.background = pygame.Surface(screenrect.size)
        self.background = self.background.convert()
        self.background.fill((250, 250, 250))

        self.screen.blit(self.background, (0,0))
        pygame.display.flip()

        self.exit_requested = False
        self.score = 0
        self.click_value = 1
        self.clock = pygame.time.Clock()

        self.images = media.load_images()
        self.sounds = media.load_sounds()
        self.crank = Crank(self.images['polar_bear'], self.sounds['beep'])
        self.allsprites = pygame.sprite.RenderPlain(self.crank)

        self.environment_image = None  # images["environment_neutral"]
        # If we want to display the score, that shouldn't be too hard. If
        # we want to display the environment only instead, that works too.
        # TODO display environment_image in background

    def update(self):
        """Called on new frame"""
        # TODO update score field, update environment image

        self.clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN
                                      and event.key == K_ESCAPE):
                self.exit_requested = True
                return
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.crank.rect.collidepoint(pos):
                    self.crank.clicked()
                    self.score += self.click_value

        self.allsprites.update()
        self.screen.blit(self.background, (0, 0))
        self.allsprites.draw(self.screen)
        pygame.display.flip()

    def play(self):
        """Begins the game. Detect any exits and exit gracefully."""
        while not self.exit_requested:
            self.update()
        pygame.quit()


def main():
    game = ClimateClicker()
    game.play()


if __name__ == "__main__":
    main()
