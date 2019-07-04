import media
import pygame
from pygame.locals import Color
from util import normalized_pos_pixels


class Machine(pygame.sprite.Sprite):
    def __init__(self,
                 name: str,
                 price: int,
                 energy_per_second: int,
                 image,
                 location: tuple,
                 ):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.name = name
        self.text_color = Color('black')
        self.price = price
        self.energy_per_second = energy_per_second
        self._count = 0
        self.image = image
        abs_location = normalized_pos_pixels(location)
        self.rect = self.image.get_rect(center=abs_location)
        self.count_sprite = pygame.sprite.Sprite()
        self.count_sprite.image = self.font.render("9", 0, self.text_color )
        self.count_sprite.rect = self.count_sprite.image.get_rect(
            center=abs_location)
        self.count = 0

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value
        count_text = self.font.render(str(value), True, self.text_color)
        self.count_sprite.image = count_text


class MachineLoader(dict):
    def __init__(self):
        self.machines = None
        self.master = None

    def load(self, master):
        self.master = master
        self.machines = {
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

    def __getitem__(self, key):
        if not self.machines:
            raise RuntimeError(
                "You must call load on machines before accessing a machine")
            # TODO more specific error
        return self.machines[key]

    def values(self):
        return self.machines.values()

    def keys(self):
        return self.machines.keys()

    def items(self):
        return self.machines.items()

    def __iter__(self):
        return iter(self.machines.keys())


machines = MachineLoader()
