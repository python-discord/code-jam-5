import pygame
from pygame.rect import Rect
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    MOUSEBUTTONDOWN,
    QUIT,
    Color
)
from media import sounds, images
from machines import machines
import time


BACKGROUND_COLOR = Color('white')
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768


def normalized_pos_pixels(normalized_position):
    if any(not 0 <= pos <= 1 for pos in normalized_position):
        raise ValueError("Normalized position must be a value between 0 and 1,"
                         "as a normalized position on screen")
    return (normalized_position[0] * SCREEN_WIDTH,
            normalized_position[1] * SCREEN_HEIGHT)


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


class ValueLabel(pygame.sprite.Sprite):
    def __init__(self, parent, x_norm, y_norm, label, units):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.label = label
        self.units = units
        self.x_norm = x_norm
        self.y_norm = y_norm
        self.font = pygame.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = Color('#222222')
        self._value = 0
        msg = f"{self.label}: {'9'*10}"  # init rect to a wide size
        self.image = self.font.render(msg, 0, self.color)
        self.rect = self.image.get_rect().move(
            *normalized_pos_pixels((self.x_norm, self.y_norm)))
        self.update()

    def update(self):
        msg = f"{self.label}: {int(self.value)} {self.units}"
        self.image = self.font.render(msg, 0, self.color)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.update()


class StaticImage(pygame.sprite.Sprite):
    def __init__(self, x_norm, y_norm, image, centered=True):
        pygame.sprite.Sprite.__init__(self)
        self.x_norm = x_norm
        self.y_norm = y_norm
        self.image = image
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.move_ip(*normalized_pos_pixels((x_norm, y_norm)))
        if centered:
            self.rect.move_ip(-self.rect.width / 2, -self.rect.height / 2)

class UpgradeButton(pygame.sprite.Sprite):
    def __init__(self, parent, x_norm, y_norm, base_cost, cost_scaling, upgrade_type, image,
                 centered=False):
        pygame.sprite.Sprite.__init__(self)
        self.x_norm = x_norm
        self.y_norm = y_norm
        self.image = image
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.move_ip(*normalized_pos_pixels((x_norm, y_norm)))
        if centered:
            self.rect.move_ip(-self.rect.width / 2, -self.rect.height / 2)

        self.upgrade_level = 0
        self.cost = base_cost
        self.cost_scaling = cost_scaling
        self.upgrade_type = upgrade_type

        self.parent = parent

        self.cost_display = ValueLabel(self, self.x_norm, self.y_norm - .03,
                                       "Cost","Joules")
        self.cost_display.value = self.cost

        self.level_display = ValueLabel(self, self.x_norm,
                                        self.y_norm - .015,
                                        "Level", "")

    def clicked(self):
        if self.parent.score >= self.cost:
            self.upgrade_level += 1
            self.parent.score -= self.cost
            self.cost *= self.cost_scaling
            self.apply_upgrades()
            self.cost_display.value = self.cost
            self.level_display.value = self.upgrade_level


    def apply_upgrades(self):
        if self.upgrade_type == "click_value":
            self.parent.click_value = 2**self.upgrade_level
            print(self.parent.click_value)
        elif self.upgrade_type == "crank_speed":
            crank = self.parent.crank
            crank.max_rotation_speed = crank.base_max_rotation_speed * (self.upgrade_level + 1)
            print(crank.max_rotation_speed)


class Crank(pygame.sprite.Sprite):
    """Hand Crank that rotates when clicked."""
    def __init__(self, parent, x_norm, y_norm, crank_images, click_sound):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.x_norm = x_norm
        self.y_norm = y_norm
        self.image = crank_images[0]
        self.crank_images = crank_images
        self.rect = self.image.get_rect()
        self.click_sound = click_sound
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.is_spinning = False
        self.spinning = 0
        self.rect.move_ip(*normalized_pos_pixels((x_norm, y_norm)))
        # The crank should center itself around its assigned screen location
        self.rect.move_ip(-self.rect.width / 2, -self.rect.height / 2)
        self.rotation_speed = 0
        self.rotation_speed_inc = .5
        self.rotation_speed_decay = .015
        self.rotation_speed_mul = 1.2
        self.rotation_speed_start = 1
        self.base_max_rotation_speed = 25
        self.max_rotation_speed = self.base_max_rotation_speed
        #self.max_rotation_speed = 1000
        self.min_rotation_speed = .5
        # When to change image based on speed
        self.speed_intervals = [0, 20, 100]

    def update(self):
        "spin based on state"
        if self.is_spinning:
            self._spin()

    def get_spin_image(self):
        index = sum(1 for threshold in self.speed_intervals
                    if self.rotation_speed >= threshold
                    ) - 1
        assert index < len(self.crank_images)
        return self.crank_images[index]

    def _spin(self):
        "Spin the sprite one full revolution"
        center = self.rect.center
        self.spinning += self.rotation_speed

        num_revolutions, self.spinning = divmod(self.spinning, 360)
        if num_revolutions:
            self.click_sound.play()
            self.parent.score += num_revolutions * self.parent.click_value

        self.image = pygame.transform.rotate(self.get_spin_image(),
                                             self.spinning)
        self.rect = self.image.get_rect(center=center)
        self.rotation_speed -= self.rotation_speed * self.rotation_speed_decay

        self.rotation_speed = max(0, min(self.rotation_speed,
                                         self.max_rotation_speed))

        if self.rotation_speed <= self.min_rotation_speed:
            self.is_spinning = False
            self.rotation_speed = 0

        self.parent.speed_sprite.value = int(self.rotation_speed / 360
                                             / self.parent.time_delta)

    def clicked(self):
        "this will cause the crank to start spinning"
        if not self.is_spinning:
            self.is_spinning = True
            self.rotation_speed = self.rotation_speed_start
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
        pygame.init()

        screenrect = Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        bestdepth = pygame.display.mode_ok(screenrect.size, 0, 32)
        self.screen = pygame.display.set_mode(screenrect.size, 0, bestdepth)
        machines.load(self)
        pygame.display.set_caption('Climate Clicker')

        self.exit_requested = False
        self.click_value = 1
        self.clock = pygame.time.Clock()

        self.background = images["environment_neutral"]
        self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        self.crank = Crank(self, 0.5, 0.5,
                           [images['crank1'],
                            images['crank2'],
                            images['crank3']
                            ],
                           sounds['snap'])
        self.crank_overlay = StaticImage(0.5, 0.5, images['crank'])
        self.upgrade_buttons = []
        self.upgrade_buttons.append(UpgradeButton(self, 0.01, 0.05,
                                                  10,
                                                  1.5,
                                                  "crank_speed",
                                                  images['upgrade_buttons1']
                                                  )
                                 )
        self.upgrade_buttons.append(UpgradeButton(self, 0.01, 0.15,
                                                  100,
                                                  10,
                                                  "click_value",
                                                  images['upgrade_buttons2']
                                                  )
                                 )

        self.score_sprite = ValueLabel(
            self, 0.02, 0.9, "Score", "Joules")
        self.speed_sprite = ValueLabel(
            self, 0.02, 0.85, "Speed", "Rotations per Second")

        self.sprite_layers = []
        self.sprite_layers.append(pygame.sprite.RenderPlain(
            self.crank
        ))
        self.sprite_layers.append(pygame.sprite.RenderPlain(
            self.crank_overlay
        ))

        # GUI layer
        self.sprite_layers.append(
            pygame.sprite.RenderPlain(
                self.score_sprite,
                self.speed_sprite,
                *self.upgrade_buttons,
                [upgrade_button.cost_display for upgrade_button in self.upgrade_buttons],
                [upgrade_button.level_display for upgrade_button in self.upgrade_buttons],
                *machines.machines.values(),
                [machine.count_sprite for machine in machines.machines.values()]
                )
            )

        # self.allsprites = pygame.sprite.RenderPlain(
        #     self.crank,
        #     self.crank_overlay,
        #     self.score_sprite,
        #     self.speed_sprite,
        #     self.upgrade_button,
        #     *machines.machines.values(),
        #     [machine.count_sprite for machine in machines.machines.values()]
        #     )
        self.last_update_time = time.time()
        self.time_delta = 0

    @property
    def energy_per_second(self):
        return sum([machine.energy_per_second * machine.count
                    for machine in machines.machines.values()])

    def update(self):
        """Called on new frame"""
        self.clock.tick(60)
        new_time = time.time()
        self.time_delta = new_time - self.last_update_time
        self.last_update_time = new_time
        self.score += self.energy_per_second * self.time_delta
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN
                                      and event.key == K_ESCAPE):
                self.exit_requested = True
                return
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.crank.rect.collidepoint(pos):
                    self.crank.clicked()
                for button in self.upgrade_buttons:
                    if button.rect.collidepoint(pos):
                        button.clicked()
                for machine in machines.machines.values():
                    if machine.rect.collidepoint(pos):
                        if self.score < machine.price:
                            sounds["beep"].play()
                        else:
                            self.score -= machine.price
                            machine.count += 1

        self.screen.fill(BACKGROUND_COLOR)
        for sprite_layer in self.sprite_layers:
            sprite_layer.update()
        #self.allsprites.update()
        self.screen.blit(self.background, (0, 0))
        for sprite_layer in self.sprite_layers:
            sprite_layer.draw(self.screen)
        #self.allsprites.draw(self.screen)
        pygame.display.flip()

    def play(self):
        """Begins the game. Detect any exits and exit gracefully."""
        while not self.exit_requested:
            self.update()
        pygame.quit()

    @property
    def score(self):
        return self.score_sprite.value

    @score.setter
    def score(self, value: int):
        self.score_sprite.value = value
        self.background = images[score_to_image(value)]


def main():
    game = ClimateClicker()
    game.play()


if __name__ == "__main__":
    main()
