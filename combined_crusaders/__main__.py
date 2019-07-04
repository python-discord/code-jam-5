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
from machines import load_machines
import time
import events
from util import in_pixels
import json


BACKGROUND_COLOR = Color('white')
SCREEN_SIZE = (1024, 768)


def say(message):
    """Sends message to the user.
    Change this method to reflect how you want the message to be sent.
    Currently just changes the program bar name cuz it's cute."""
    if message is not None:
        pygame.display.set_caption(str(message))


if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")


def score_to_image(score: int):
    # TODO there must be a cleaner way to do this, especially when we have
    # more than just 3 states
    if score < 10000:
        return "environment_negative"
    elif score >= 10000 and score < 500000:
        return "environment_neutral"
    elif score >= 500000:
        return "environment_positive"
    raise RuntimeError("Score didn't make sense")


class TextButton(pygame.sprite.Sprite):
    def __init__(self, coords, text, on_click,
                 font=None, color=Color('#222222')):
        pygame.sprite.Sprite.__init__(self)
        font = font or pygame.font.Font(None, 20)
        self.on_click = on_click
        self.image = font.render(text, 0, color)
        self.rect = self.image.get_rect().move(*in_pixels(coords))


class ValueLabel(pygame.sprite.Sprite):
    def __init__(self, coords, label, units):
        pygame.sprite.Sprite.__init__(self)
        self.label = label
        self.units = units
        self.coords = coords
        self.font = pygame.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = Color('#222222')
        self._value = 0
        msg = f"{self.label}: {'9'*10}"  # init rect to a wide size
        self.image = self.font.render(msg, 0, self.color)
        self.rect = self.image.get_rect().move(*in_pixels(self.coords))
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
    def __init__(self, coords, image, centered=True):
        pygame.sprite.Sprite.__init__(self)
        self.coords = coords
        self.image = image
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.move_ip(*in_pixels(coords))
        if centered:
            self.rect.move_ip(-self.rect.width / 2, -self.rect.height / 2)


class UpgradeButton(pygame.sprite.Sprite):
    def __init__(self, parent, coords, base_cost, cost_scaling,
                 upgrade_type, image, centered=False):
        pygame.sprite.Sprite.__init__(self)
        self.coords = coords
        self.image = image
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.move_ip(*in_pixels(coords))
        if centered:
            self.rect.move_ip(-self.rect.width / 2, -self.rect.height / 2)

        self._level = 0
        self.base_cost = base_cost
        self.cost = self.base_cost
        self.cost_scaling = cost_scaling
        self.upgrade_type = upgrade_type

        self.parent = parent

        self.cost_display = ValueLabel((self.coords[0], self.coords[1]-.03),
                                       "Cost", "Joules")
        self.cost_display.value = self.cost

        self.level_display = ValueLabel((self.coords[0], self.coords[1]-.015),
                                        "Level", "")

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value
        self.cost = self.base_cost*(self.cost_scaling**self.level)
        self.apply_upgrades()
        self.cost_display.value = self.cost
        self.level_display.value = self.level

    def clicked(self):
        if self.parent.score >= self.cost:
            self.parent.score -= self.cost
            self.level += 1
            self.parent.events.send(f"buy_upgrade_{self.upgrade_type}")

    def apply_upgrades(self):
        if self.upgrade_type == "click_value":
            self.parent.click_value = 2**self.level
        elif self.upgrade_type == "crank_speed":
            self.parent.crank.max_rotation_speed = (
                self.parent.crank.base_max_rotation_speed
                * (self.level + 1))
        elif self.upgrade_type == "crank_inertia":
            if not self.level:
                self.parent.crank_rotation_speed_decay = (
                     self.parent.crank.rotation_speed_base_decay)
            else:
                self.parent.crank.rotation_speed_decay = (
                    self.parent.crank.rotation_speed_base_decay
                    * (.1 + (.9 / self.level)))


class Crank(pygame.sprite.Sprite):
    """Hand Crank that rotates when clicked."""
    def __init__(self, parent, coords, crank_images, click_sound):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.coords = coords
        self.image = crank_images[0]
        self.crank_images = crank_images
        self.rect = self.image.get_rect()
        self.click_sound = click_sound
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.is_spinning = False
        self.spinning = 0
        self.rect.move_ip(*in_pixels(coords))
        # The crank should center itself around its assigned screen location
        self.rect.move_ip(-self.rect.width / 2, -self.rect.height / 2)
        self.rotation_speed = 0
        self.rotation_speed_inc = .5
        self.rotation_speed_base_decay = .015
        self.rotation_speed_decay = self.rotation_speed_base_decay
        self.rotation_speed_mul = 1.2
        self.rotation_speed_start = 1
        self.base_max_rotation_speed = 25
        self.max_rotation_speed = self.base_max_rotation_speed
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
        self.parent.events.send("crank")
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

        screenrect = Rect(0, 0, *SCREEN_SIZE)
        bestdepth = pygame.display.mode_ok(screenrect.size, 0, 32)
        self.screen = pygame.display.set_mode(screenrect.size, 0, bestdepth)
        self.machines = load_machines()
        pygame.display.set_caption('Climate Clicker')

        self.exit_requested = False
        self.click_value = 1
        self.clock = pygame.time.Clock()

        self.background = images["environment_neutral"]
        self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        self.crank = Crank(self, (0.5, 0.5),
                           [images['crank1'],
                            images['crank2'],
                            images['crank3']
                            ],
                           sounds['snap'])
        self.crank_overlay = StaticImage((0.5, 0.5), images['crank'])
        self.upgrade_buttons = [
            UpgradeButton(self, (0.01, 0.05), 10, 1.5, "crank_speed",
                          images['upgrade_buttons1']),
            UpgradeButton(self, (0.01, 0.15), 100, 10, "click_value",
                          images['upgrade_buttons2']),
            UpgradeButton(self, (0.01, 0.25), 100, 2, "crank_inertia",
                          images['upgrade_buttons3'])
        ]

        self.save_button = TextButton((0.4, 0.1), "Save", self.save)
        self.load_button = TextButton((0.6, 0.1), "Load", self.load)
        self.text_buttons = (self.save_button, self.load_button)

        self.score_sprite = ValueLabel(
            (0.02, 0.9), "Score", "Joules")
        self.speed_sprite = ValueLabel(
            (0.02, 0.85), "Speed", "Rotations per Second")

        gui_plain = pygame.sprite.RenderPlain(
            self.score_sprite,
            self.speed_sprite,
            *self.upgrade_buttons,
            [button.cost_display for button in self.upgrade_buttons],
            [button.level_display for button in self.upgrade_buttons],
            *self.machines.values(),
            [machine.count_sprite for machine in self.machines.values()],
            self.text_buttons
        )
        self.sprite_layers = [
            pygame.sprite.RenderPlain(self.crank),
            pygame.sprite.RenderPlain(self.crank_overlay),
            gui_plain
        ]
        self.events = events.Events(self)
        self.last_update_time = time.time()
        self.time_delta = 0

    @property
    def energy_per_second(self):
        return sum([machine.energy_per_second * machine.count
                    for machine in self.machines.values()])

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
                for machine in self.machines.values():
                    if machine.rect.collidepoint(pos):
                        if self.score < machine.price:
                            sounds["beep"].play()
                        else:
                            self.score -= machine.price
                            machine.count += 1
                            self.events.send(f"buy_machine_{machine.name}")
                for button in self.text_buttons:
                    if button.rect.collidepoint(pos):
                        button.on_click()

        self.screen.fill(BACKGROUND_COLOR)
        for sprite_layer in self.sprite_layers:
            sprite_layer.update()
        self.screen.blit(self.background, (0, 0))
        for sprite_layer in self.sprite_layers:
            sprite_layer.draw(self.screen)
        pygame.display.flip()
        say(self.events.get_current_message())

    def play(self):
        """Begins the game. Detect any exits and exit gracefully."""
        while not self.exit_requested:
            self.update()
        pygame.quit()

    def as_dict(self):
        return {
            "score": self.score,
            "machine_count": {machine_name: machine.count
                              for machine_name, machine in self.machines.items()},
            "upgrade_level": {
                upgrade.upgrade_type: upgrade.level
                for upgrade in self.upgrade_buttons
            }
        }

    def load_data(self, data):
        self.score = data["score"]
        for machine, machine_count in data["machine_count"].items():
            self.machines[machine].count = machine_count
        for upgrade in self.upgrade_buttons:
            upgrade.level = data["upgrade_level"][upgrade.upgrade_type]

    def save(self):
        with open("savefile.json", "w") as savefile:
            as_dict = self.as_dict()
            print(as_dict)
            json.dump(as_dict, savefile)

    def load(self):
        with open("savefile.json", "r") as savefile:
            save_data = json.load(savefile)
        self.load_data(save_data)

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
