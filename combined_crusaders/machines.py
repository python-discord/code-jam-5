import media
import pygame
from pygame.locals import Color
from util import in_pixels


class Machine(pygame.sprite.Sprite):
    def __init__(self,
                 name: str,
                 price: int,
                 energy_per_second: int,
                 image,
                 coords: tuple,
                 ):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.name = name
        self.text_color = Color('black')
        self.price = price
        self.energy_per_second = energy_per_second
        self._count = 0
        self.image = image
        abs_coords = in_pixels(coords)
        self.rect = self.image.get_rect(center=abs_coords)
        self.count_sprite = pygame.sprite.Sprite()
        self.count_sprite.image = self.font.render("9", 0, self.text_color )
        self.count_sprite.rect = self.count_sprite.image.get_rect(
            center=abs_coords)
        self.count = 0

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value
        count_text = self.font.render(str(value), True, self.text_color)
        self.count_sprite.image = count_text


def load_machines():
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
