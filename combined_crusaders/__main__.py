import pygame
from pygame.rect import Rect
from pygame.locals import KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, QUIT, Color
from media import sounds, images
from machines import load_machines
import time
import events
from util import in_pixels, in_norm
import json


if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")


def say(message) -> None:
    """Send a message to the user.
    Currently just changes the program bar name cuz it's cute.

    :param message: Message to display.
    :type message: Does not require type str, but must be castable to str.

    """
    if message is not None:
        pygame.display.set_caption(str(message))


def score_to_image(score: int) -> str:
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
    def __init__(self, coords, text, clicked,
                 font=None, color=Color('#222222')):
        """Button that displays text and performs an action on click.
        clicked: Function to run when the button is clicked
        image: Font with a rendered version of the button text
        rect: pygame rect representing the button's boundaries
        """
        pygame.sprite.Sprite.__init__(self)
        font = font or pygame.font.Font(None, 20)
        self.clicked = clicked
        self.image = font.render(text, 0, color)
        self.rect = self.image.get_rect().move(*in_pixels(coords))


class ValueLabel(pygame.sprite.Sprite):
    """Label that displays text in the form {descriptor}: {value} {units}
    descriptor, value, units: the parts of the label (see above)
    coords: Normalized location of the label
    font: pygame font to use when displaying the label
    color: pygame color to use when displaying the label
    update: Function to reflect changes in properties onto the UI
    rect: pygame rect representing the label's boundaries
    """
    def __init__(self, coords, descriptor, units):
        pygame.sprite.Sprite.__init__(self)
        self.descriptor = descriptor
        self.coords = coords
        self.units = units
        self.font = pygame.font.SysFont("SegoeUI", 18)
        self.font.set_bold(1)
        self.color = Color('#ffffff')
        self._value = 0
        self.update()
        self.rect = self.image.get_rect()
        self.rect.move_ip(*in_pixels(self.coords))
        self.update()

    def update(self):
        """Update rendered text to match changes to object"""
        text = f"{self.descriptor}: {int(self.value)} {self.units}"
        self.image = self.font.render(text, 0, self.color)

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int):
        self._value = value
        self.update()


class StaticImage(pygame.sprite.Sprite):
    """Image displayed on pygame window.
    coords: Normalized location of the image
    image: pygame image to be displayed
    rect: pygame rect representing the image's boundaries
    """
    def __init__(self, coords, image, centered=True):
        pygame.sprite.Sprite.__init__(self)
        self.coords = coords
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.move_ip(*in_pixels(self.coords))
        if centered:
            self.rect.move_ip(-self.rect.w / 2, -self.rect.h / 2)


class UpgradeButton(pygame.sprite.Sprite):
    """Button to upgrade a property of the crank.
    coords: Normalized location of the button
    image: pygame image to be displayed on the button's surface
    rect: pygame rect representing the image's boundaries
    base_cost: Initial cost of the upgrade
    cost: Current cost of the upgrade
    cost_scaling: Logarithmic base to use when calculating cost from base_cost
    type: The type of upgrade
        Should be one of ["click_value", "crank_speed", "crank_inertia"]
    parent: The parent object, of class ClimateClicker
    cost_display: pygame display for the cost of the upgrade
    level_display: pygame display for the level of the upgrade
    level: Current level of the upgrade
    """
    def __init__(self, parent, coords, base_cost, cost_scaling,
                 type, image, centered=False):
        pygame.sprite.Sprite.__init__(self)
        self.coords = coords
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.move_ip(*in_pixels(coords))
        if centered:
            self.rect.move_ip(-self.rect.w / 2, -self.rect.h / 2)

        self._level = 0
        self.base_cost = base_cost
        self.cost = self.base_cost
        self.cost_scaling = cost_scaling
        self.type = type

        self.parent = parent

        line_height = pygame.font.SysFont("SegoeUI", 18).get_linesize() * .75

        cost_coords = in_norm((self.rect.x, self.rect.y - (self.rect.h/2)))
        self.cost_display = ValueLabel(cost_coords, "Cost", "Joules")
        self.cost_display.value = self.cost

        level_coords = in_norm((self.rect.x,
                                self.rect.y - (self.rect.h/2) - line_height))
        self.level_display = ValueLabel(level_coords, "Level", "")

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int):
        self._level = value
        self.cost = self.base_cost*(self.cost_scaling**self.level)
        self.apply_upgrades()
        self.cost_display.value = self.cost
        self.level_display.value = self.level

    def clicked(self):
        """Called when UI button is clicked. Purchase upgrade.
        If user does not have enough joules, silently pass."""
        if self.parent.score >= self.cost:
            self.parent.score -= self.cost
            self.level += 1
            self.parent.events.send(f"buy_upgrade_{self.type}")

    def apply_upgrades(self):
        """Given a change in upgrade level, reflect changes in the crank"""
        if self.type == "click_value":
            self.parent.click_value = 2**self.level
        elif self.type == "crank_speed":
            self.parent.crank.max_rotation_speed = (
                self.parent.crank.base_max_rotation_speed
                * (self.level + 1))
        elif self.type == "crank_inertia":
            if not self.level:
                self.parent.crank_rotation_speed_decay = (
                    self.parent.crank.rotation_speed_base_decay)
            else:
                self.parent.crank.rotation_speed_decay = (
                    self.parent.crank.rotation_speed_base_decay
                    * (.1 + (.9 / self.level)))


class Crank(pygame.sprite.Sprite):
    """Hand Crank that rotates when clicked.
    parent: Parent object, of class ClimateClicker
    coords: Normalized location of the crank
    image: Crank image base
    crank_images: dynamic images for different speeds of the crank
        Selected by current threshold of speed_intervals
    rect: pygame rect representing the image's boundaries
    click_sound: pygame sound to play when the crank completes a rotation
    is_spinning: Whether the crank is in motion
    rotation: The current rotation of the crank in degrees.
        May exceed 360 if a rotation was completed in the previous frame
    rotation_speed: Current rate of degrees/frame
    rotation_speed_inc: The rotation speed to increase when clicked
        Used along with rotation_speed_mul, before mul has been calculated
    rotation_speed_base_decay: Initial rotation speed constant decrease
    rotation_speed_decay: Curent rotation speed constant decrease
    rotation_speed_mul: The rotation speed to multiple when clicked.
        Used along with rotation_speed_inc, after inc has been calculated
    rotation_speed_start: How fast to rotate on the first click
    base_max_rotation_speed: Initial maximum speed for rotation
    max_rotation_speed: Current maximum speed for rotation
    min_rotation_speed: Minimum speed for rotation (stop rotation if lower)
    speed_intervals: Thresholds for when the crank image should change
        Adjusts crank_images active index
    """
    def __init__(self, parent, coords, crank_images, click_sound):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.coords = coords
        self.image = crank_images[0]
        self.crank_images = crank_images
        self.rect = self.image.get_rect()
        self.click_sound = click_sound
        self.is_spinning: bool = False
        self.rotation = 0
        self.rect.move_ip(*in_pixels(coords))
        # The crank should center itself around its assigned screen location
        self.rect.move_ip(-self.rect.w / 2, -self.rect.h / 2)
        self.rotation_speed = 0
        self.rotation_speed_inc = .5
        self.rotation_speed_base_decay = .015
        self.rotation_speed_decay = self.rotation_speed_base_decay
        self.rotation_speed_mul = 1.2
        self.rotation_speed_start = 1
        self.base_max_rotation_speed = 25
        self.max_rotation_speed = self.base_max_rotation_speed
        self.min_rotation_speed = .5
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
        "Spin the sprite for one frame"
        center = self.rect.center
        self.rotation += self.rotation_speed
        num_revolutions, self.rotation = divmod(self.rotation, 360)
        if num_revolutions:
            self.click_sound.play()
            self.parent.score += num_revolutions * self.parent.click_value

        self.image = pygame.transform.rotate(self.get_spin_image(),
                                             self.rotation)
        self.rect = self.image.get_rect(center=center)
        self.rotation_speed -= self.rotation_speed * self.rotation_speed_decay

        self.rotation_speed = max(0, min(self.rotation_speed,
                                         self.max_rotation_speed))

        if self.rotation_speed <= self.min_rotation_speed:
            self.is_spinning = False
            self.rotation_speed = 0

        self.parent.speed = int(self.rotation_speed / 360
                                / self.parent.time_delta)

    def clicked(self):
        "Called when user clicks the crank. Incrase crank speed."
        self.parent.events.send("crank")
        if not self.is_spinning:
            self.is_spinning = True
            self.rotation_speed = self.rotation_speed_start
        else:
            self.rotation_speed += self.rotation_speed_inc
            self.rotation_speed *= self.rotation_speed_mul


class ClimateClicker:
    """Main game class.
    screen: pygame active display
    machines: Collection of machine data with their count and cost
    exit_requested: Whether an exit has been requested by user (exit if so)
    click_value: How many joules to generate after a crank rotation
    clock: Game clock, for limiting FPS
    background: Currently active background image
    overlay1: Canvas for displays further back
    overlay2: Canvas for displays closer to the front
    overlay_color: pygame color to use for the overlay
    crank: crank object for generating joules
    crank_overlay: crank-specific overlay
    upgrade_buttons: Buttons to upgrade crank properties
    save_button: Button used to save game
    load_button: Button used to load a saved game
    score_sprite: Rendered font showing the current score
    speed_sprite: Rendered font showing the current speed
    sprite_layers: Layers of the display to draw
    events: Events object, for remembering history
    last_update_time: Unix time of last frame
    time_delta: Seconds since last frame
    energy_per_second: Current watts from machines only; readonly
    all_buttons: Helper collection of all buttons (text and upgrade)
    score: Current score in watts
    speed: Current speed in revolutions per second

    """
    def __init__(self, screen_size=(1024, 768), bg_color=Color('white')):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()

        screenrect = Rect(0, 0, *screen_size)
        bestdepth = pygame.display.mode_ok(screenrect.size, 0, 32)
        self.screen = pygame.display.set_mode(screenrect.size, 0, bestdepth)
        self.machines = load_machines()
        pygame.display.set_caption('Climate Clicker')

        self.exit_requested = False
        self.click_value = 1
        self.clock = pygame.time.Clock()

        self.background = images["environment_neutral"]
        self.screen.fill(bg_color)
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        self.overlay1 = pygame.Rect(0, 0, 200, 600)
        self.overlay2 = pygame.Rect(0, 650, 300, 150)
        self.overlay_color = Color("#222222")
        self.crank = Crank(self, (0.5, 0.5),
                           [images['crank1'],
                            images['crank2'],
                            images['crank3']
                            ],
                           sounds['snap'])
        self.crank_overlay = StaticImage((0.5, 0.5), images['crank'])
        self.upgrade_buttons = (
            UpgradeButton(self, (0.01, 0.05), 10, 1.5, "crank_speed",
                          images['upgrade_buttons1']),
            UpgradeButton(self, (0.01, 0.175), 100, 10, "click_value",
                          images['upgrade_buttons2']),
            UpgradeButton(self, (0.01, 0.3), 100, 2, "crank_inertia",
                          images['upgrade_buttons3'])
        )

        self.save_button = TextButton((0.4, 0.1), "Save", self.save)
        self.load_button = TextButton((0.6, 0.1), "Load", self.load)
        text_buttons = (self.save_button, self.load_button)
        self.all_buttons = self.upgrade_buttons + text_buttons

        self.score_sprite = ValueLabel(
            (0.02, 0.9), "Score", "Joules")
        self.speed_sprite = ValueLabel(
            (0.02, 0.85), "Speed", "Rotations per Second")

        gui_plain = pygame.sprite.RenderPlain(
            self.score_sprite,
            self.speed_sprite,
            self.all_buttons,
            [button.cost_display for button in self.upgrade_buttons],
            [button.level_display for button in self.upgrade_buttons],
            *self.machines.values(),
            [machine.count_sprite for machine in self.machines.values()],
            [machine.cost_sprite for machine in self.machines.values()],

        )
        self.sprite_layers = (
            pygame.sprite.RenderPlain(self.crank),
            pygame.sprite.RenderPlain(self.crank_overlay),
            gui_plain
        )
        self.events = events.Events(self)
        self.last_update_time = time.time()
        self.time_delta = 0

    @property
    def energy_per_second(self):
        return sum([machine.energy_per_second * machine.count
                    for machine in self.machines.values()])

    def update(self):
        """Called on new frame."""
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
                for button in self.all_buttons:
                    if button.rect.collidepoint(pos):
                        button.clicked()
                for machine in self.machines.values():
                    if machine.rect.collidepoint(pos):
                        if self.score >= machine.cost:
                            self.score -= machine.cost
                            machine.count += 1
                            self.events.send(f"buy_machine_{machine.name}")

        for sprite_layer in self.sprite_layers:
            sprite_layer.update()
        self.screen.blit(self.background, (0, 0))
        self.screen.fill(self.overlay_color, rect=self.overlay1, special_flags=pygame.BLEND_MULT)
        self.screen.fill(self.overlay_color, rect=self.overlay2, special_flags=pygame.BLEND_MULT)
        for sprite_layer in self.sprite_layers:
            sprite_layer.draw(self.screen)
        pygame.display.flip()
        say(self.events.get_current_message())

    def play(self):
        """Begin the game. Detect any exits and exit gracefully."""
        while not self.exit_requested:
            self.update()
        pygame.quit()

    def as_dict(self):
        """Get a serialized version of the game state, for saving"""
        return {
            "score": self.score,
            "machine_count": {
                machine_name: machine.count
                for machine_name, machine in self.machines.items()},
            "upgrade_level": {
                upgrade.type: upgrade.level
                for upgrade in self.upgrade_buttons},
            "history": self.events.event_list
        }

    def load_data(self, data: dict):
        """Update the game state with the save data."""
        self.score = data["score"]
        for machine, machine_count in data["machine_count"].items():
            self.machines[machine].count = machine_count
        for upgrade in self.upgrade_buttons:
            upgrade.level = data["upgrade_level"][upgrade.type]
        self.events.event_list = data["history"]

    def save(self):
        """Save current game data to a file"""
        with open("save_file.json", "w") as save_file:
            save_data = self.as_dict()
            json.dump(save_data, save_file)
        self.events.send("save")

    def load(self):
        """Restore current game data from a file"""
        try:
            with open("save_file.json", "r") as save_file:
                save_data = json.load(save_file)
        except FileNotFoundError:
            self.events.send("fail_load")
        else:
            self.load_data(save_data)
            self.events.send("load")

    @property
    def score(self):
        return self.score_sprite.value

    @score.setter
    def score(self, value: int):
        self.score_sprite.value = value
        self.background = images[score_to_image(value)]

    @property
    def speed(self):
        return self.speed_sprite.value

    @speed.setter
    def speed(self, value):
        self.speed_sprite.value = value


def main():
    game = ClimateClicker()
    game.play()


if __name__ == "__main__":
    main()
