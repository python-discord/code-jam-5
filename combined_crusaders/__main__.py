# Some of this skeleton was stolen from the aliens pygame example
import pygame
from pygame.rect import Rect
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    MOUSEBUTTONDOWN,
    QUIT,
    Color
)
import media


BACKGROUND_COLOR = Color('white')


if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")


def score_to_image(score: int):
    # TODO there must be a cleaner way to do this, especially when we have
    # more than just 3 states
    if score < 0:
        return "environment_negative"
    elif score == 0:
        return "environment_neutral"
    elif score > 0:
        return "environment_positive"
    raise RuntimeError("Score didn't make sense")


class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = Color('grey')
        self.score_val = 0
        msg = f"Score: {'9'*10}"  # init rect to a wide size
        self.image = self.font.render(msg, 0, self.color)
        self.rect = self.image.get_rect().move(10, 450)
        self.update()

    def update(self):
        msg = f"Score: {self.score_val}"
        self.image = self.font.render(msg, 0, self.color)


class Crank(pygame.sprite.Sprite):
    """Hand Crank that rotates when clicked."""
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
            self.click_sound.play()
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
            # self.click_sound.play()
            self.spinning = 1
            self.original = self.image


class ClimateClicker:
    """Class should hold information about state of game
    This includes current environment value and such.
    Sprites and such should probably be held at class-level or module-level
     instead? maybe? idk lol
    """
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()

        screenrect = Rect(0, 0, 640, 480)
        bestdepth = pygame.display.mode_ok(screenrect.size, 0, 32)
        self.screen = pygame.display.set_mode(screenrect.size, 0, bestdepth)
        pygame.display.set_caption('Climate Clicker')

        self.exit_requested = False
        self.click_value = 1
        self.clock = pygame.time.Clock()

        self.images = media.load_images()
        self.sounds = media.load_sounds()

        self.background = self.images["environment_neutral"]
        self.background = self.background.convert()
        self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        self.crank = Crank(self.images['polar_bear'], self.sounds['snap'])
        self.score_sprite = Score()
        self.allsprites = pygame.sprite.RenderPlain(self.crank,
                                                    self.score_sprite)

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

    @property
    def score(self):
        return self.score_sprite.score_val

    @score.setter
    def score(self, value: int):
        self.score_sprite.score_val = value
        self.screen.fill(BACKGROUND_COLOR, rect=self.score_sprite.rect)
        self.score_sprite.update()
        self.background = self.images[score_to_image(value)]


def main():
    game = ClimateClicker()
    game.play()


if __name__ == "__main__":
    main()
