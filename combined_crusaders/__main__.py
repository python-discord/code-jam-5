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
import math


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
    def __init__(self, parent, x, y, label):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.label = label
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = Color('grey')
        self.score_val = 0
        msg = f"{self.label}: {'9'*10}"  # init rect to a wide size
        self.image = self.font.render(msg, 0, self.color)
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.update()

    def update(self):
        msg = f"{self.label}: {self.score_val}"
        self.parent.screen.fill(BACKGROUND_COLOR, rect=self.rect)
        self.image = self.font.render(msg, 0, self.color)

    def change_value(self, value):
        self.score_val = value
        self.update()

class StaticImage(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.move_ip(x, y)

class Crank(pygame.sprite.Sprite):
    """Hand Crank that rotates when clicked."""
    def __init__(self, parent, x, y, crank_images, click_sound):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.x = x
        self.y = y
        self.image = crank_images[0]
        self.crank_images = crank_images
        self.rect = self.image.get_rect()
        self.click_sound = click_sound
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.is_spinning = False
        self.spinning = 0
        self.rect.move_ip(x, y)
        self.rotation_speed = 0
        self.rotation_speed_inc = .5
        self.rotation_speed_decay = .015
        self.rotation_speed_mul = 1.2
        self.rotation_speed_start = 1
        self.max_rotation_speed = 1000
        self.min_rotation_speed = .5
        # When to change image based on speed
        self.speed_intervals = [0, 20, 100]

    def update(self):
        "spin based on state"
        if self.is_spinning:
            self._spin()
        # else:
        #     self.image = self.crank_images[0]
        #     self.rect = self.image.get_rect()
        #     self.rect.move_ip(self.x, self.y)

    def get_spin_image(self):
        index = sum(1 for threshold in self.speed_intervals
                    if self.rotation_speed >= threshold
                    ) - 1
        #print(index)
        assert index < len(self.crank_images)
        return self.crank_images[index]

    def _spin(self):
        "Spin the sprite one full revolution"
        center = self.rect.center
        self.spinning += self.rotation_speed
        while self.spinning >= 360:
            self.spinning -=360
            self.parent.score += self.parent.click_value

        self.image = pygame.transform.rotate(self.get_spin_image(),
                                             self.spinning)
        self.rect = self.image.get_rect(center=center)
        self.rotation_speed -= self.rotation_speed * self.rotation_speed_decay

        self.rotation_speed = max(0, min(self.rotation_speed, self.max_rotation_speed))

        if self.rotation_speed <= self.min_rotation_speed:
            self.is_spinning = False
            self.rotation_speed = 0

        self.parent.speed_sprite.change_value(math.floor(self.rotation_speed))

    def clicked(self):
        "this will cause the crank to start spinning"
        if not self.is_spinning:
            # self.click_sound.play()
            self.is_spinning = True
            self.rotation_speed = self.rotation_speed_start
            #self.original = self.image
        else:
            self.rotation_speed += self.rotation_speed_inc
            self.rotation_speed *= self.rotation_speed_mul


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
        #self.background = self.background.convert()
        self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        self.crank = Crank(self, 100, 100,
                           [self.images['crank1'],
                            self.images['crank2'],
                            self.images['crank3']],
                           self.sounds['beep'])
        self.crank_overlay = StaticImage(100, 100, self.images['crank'])
        self.score_sprite = Score(self, 10, 450, "Score")
        self.speed_sprite = Score(self, 10, 400, "Speed")
        self.allsprites = pygame.sprite.RenderPlain(self.crank,
                                                    self.crank_overlay,
                                                    self.score_sprite,
                                                    self.speed_sprite)

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
                    #self.score += self.click_value

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
        self.score_sprite.change_value(value)
        self.background = self.images[score_to_image(value)]


def main():
    game = ClimateClicker()
    game.play()


if __name__ == "__main__":
    main()
