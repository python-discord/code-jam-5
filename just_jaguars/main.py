import pygame
from assets import *

window_width = 1320
window_height = 720
window_icon = None
window_title = 'Name of game'

fps = 60

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

fossil_fuel_types = ('natural gas', oil, 'coal')
green_energy_types = ('solar', 'wind', 'hydro', 'geothermal',
                      'biomass', 'nuclear', 'hydrogen fuel cells')


class Icon(pygame.sprite.Sprite):
    def __init__(self, energy_source, left_coordinate):
        pygame.sprite.Sprite.__init__(self)
        self.image = energy_source
        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        self.rect.left = left_coordinate
        self.clicked = False
        if energy_source in fossil_fuel_types:
            self.type = 'fossil fuel'
        elif energy_source in green_energy_types:
            self.type = 'green energy'

    def update(self):
        self.rect.y += 5
        if self.rect.top > window_height:
            self.rect.bottom = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                print(f'You clicked on a {self.type} icon!')
                icon.kill()


pygame.init()

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(window_title)
clock = pygame.time.Clock()

all_icons = pygame.sprite.Group()
icon = Icon(oil, window_width / 2)
all_icons.add(icon)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_icons.update()

    window.fill(white)

    all_icons.draw(window)

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
