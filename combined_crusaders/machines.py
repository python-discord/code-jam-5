import media
import pygame
from pygame.locals import Color


machines = None


class Machine(pygame.sprite.Sprite):
    def __init__(self,
                 price: int,
                 energy_per_second: int,
                 image,
                 location: tuple,
                 ):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.price = price
        self.energy_per_second = energy_per_second
        self._count = 0
        self.image = image
        self.rect = self.image.get_rect(center=location)
        self.count_sprite = pygame.sprite.Sprite()
        self.count_sprite.image = self.font.render("9", 0, Color('black'))
        self.count_sprite.rect = self.count_sprite.image.get_rect(
            center=location)
        self.count = 0

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value
        count_text = self.font.render(str(value), True, Color('black'))
        self.count_sprite.image = count_text


def init():
    global machines
    machines = {"solar_panel": Machine(10, 0.2,
                                       media.images["solar_panel"],
                                       (500, 100),
                                       ),
                "wind_turbine": Machine(50, 0.5,
                                        media.images["wind_turbine"],
                                        (550, 100),
                                        )
                }
