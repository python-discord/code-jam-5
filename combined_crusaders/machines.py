"""Module to deal with organization of machines.
'Machines' references the purchasable items which produce energy over time.
"""
import pygame
from pygame.locals import Color
from util import in_pixels
import media


class Machine(pygame.sprite.Sprite):
    """Holds information about machines
    font: pygame font to use for text on the machine button
    name: name of the machine
    text_color: pygame color to use for text on the machine button
    cost: Cost of the machine in Joules
    energy_per_second: Wattage of one unit of the machine
    image: pygame image to use on the machine button
    rect: pygame rect representing the machine button's boundaries
    count_sprite: Rendered text displaying the number of a given machine
    cost_sprite: Rendered text displaying the cost of a given machine
    count: The count of a given machine (how many there are)
    """
    def __init__(self, name: str, cost: int, energy_per_second: int,
                 image, coords: tuple):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.name = name
        self.text_color = Color('black')
        self.cost = cost
        self.energy_per_second = energy_per_second
        self._count = 0
        self.image = image
        abs_coords = in_pixels(coords)
        self.rect = self.image.get_rect(center=abs_coords)
        self.count_sprite = pygame.sprite.Sprite()
        self.count_sprite.image = self.font.render("0", 0, self.text_color)
        count_coords_abs = (self.rect.x, self.rect.y + self.rect.h)
        self.count_sprite.rect = self.count_sprite.image.get_rect(
            center=count_coords_abs)
        self.cost_sprite = pygame.sprite.Sprite()
        self.cost_sprite.image = self.font.render(
            f"{self.cost} Joules", 0, self.text_color)
        cost_coords_abs = (
            self.count_sprite.rect.x,
            self.count_sprite.rect.y + 2 * self.count_sprite.rect.h)
        self.cost_sprite.rect = self.count_sprite.image.get_rect(
            center=cost_coords_abs)
        self.count = 0

    @property
    def count(self):
        """Number of machines of a given type currently owned"""
        return self._count

    @count.setter
    def count(self, value):
        self._count = value
        count_text = self.font.render(str(value), True, self.text_color)
        self.count_sprite.image = count_text


def load_machines():
    """Get the default machines"""
    return {
        "solar_panel": Machine("solar_panel",
                               60,
                               0.5,
                               media.images["solar_panel"],
                               (0.8, 0.2)),
        "wind_turbine": Machine("wind_turbine",
                                90,
                                2,
                                media.images["wind_turbine"],
                                (0.9, 0.2))
    }
