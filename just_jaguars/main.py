import pygame

from assets import (
    natural_gas, oil, coal,
    solar, wind, hydro,
    geothermal, biomass, nuclear,
    hydrogen, ghg_capture_tech
)  # Importing the images for the icons
from random import randint, choice
from time import time

# Details about the window
window_width = 1152
aspect_ratio = 9/16
window_height = int(aspect_ratio*window_width)
window_icon = None
window_title = 'Name of game'

fps = 60

# Fonts
pygame.font.init()
arial = pygame.font.SysFont('Arial MT', 30)

# Colors used
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

icon_speed = 2  # The speed at which the icons fall down the screen, x-pixels per frame.

"""
The following are the two energy types an icon can be, which energy sources
fall into those types, as well as a greenhouse gas capture technology type.
"""
fossil_fuel_types = (natural_gas, oil, coal)
green_energy_types = (solar, wind, hydro, geothermal,
                      biomass, nuclear, hydrogen)
ghg_capture_technology = ghg_capture_tech


class Icon(pygame.sprite.Sprite):
    def __init__(self, energy_source, left_coordinate):
        """
        Each icon has an image, an energy source, an energy type, and an
        x-coordinate. Newly generated icons always start at the top of
        the screen, i.e. their initial y-coordinates are always 0.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = energy_source
        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        self.rect.left = left_coordinate
        if energy_source in fossil_fuel_types:
            self.type = 'fossil fuel'
            self.energy_output = 10
            self.emission_output = 10
        elif energy_source in green_energy_types:
            self.type = 'green energy'
            self.energy_output = 1
            self.emission_output = 0
        elif energy_source == ghg_capture_tech:
            self.type = 'ghg capture tech'
            self.energy_output = 0
            self.emission_output = 0

    def update(self):
        """
        Every frame each icon falls down the screen at the specified
        speed. When it reaches the bottom it is removed.
        """
        self.rect.y += icon_speed
        if self.rect.top > window_height:
            self.kill()


def icon_clicked(event):
    """This runs if an icon is clicked."""
    mouse_position = pygame.mouse.get_pos()
    for icon in all_icons:
        if icon.rect.collidepoint(mouse_position):
            if event.button == 1:  # Left-click
                print(f'You LEFT clicked on a {icon.type} icon! '
                      f'It has an energy output of {icon.energy_output} '
                      f'and an emission output of {icon.emission_output}.')
                icon.kill()
            elif event.button == 3:  # Right-click
                print(f'You RIGHT clicked on a {icon.type} icon! '
                      f'It has an energy output of {icon.energy_output} '
                      f'and an emission output of {icon.emission_output}.')
                icon.kill()
            else:
                pass


# Boiler-plate:
pygame.init()
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(window_title)
clock = pygame.time.Clock()

all_icons = pygame.sprite.Group()  # All icons on the screen are put into this Group object.

"""
The following variables are used to generalize the spacing and layout of
the icons relative to window size and the chosen number of icons in a row.
Hard coding in the positions of the icons would make future changes to
window size or number of icons in a row difficult because you would also
have to go back and recalculate all the icons' new positions.
"""
number_of_icons_in_a_row = 8
icon_width = 64
icon_area_width = 2 * window_width / 3  # Width of area containing the icons
total_space_between_icons = icon_area_width - number_of_icons_in_a_row * icon_width
# Spacing between individual icons (below)
icon_spacing = total_space_between_icons / number_of_icons_in_a_row
first_x_coordinate = window_width / 3  # The x-coordinate of the first icon in a row

"""
This list keeps track of all the rows created. It is used to create the
first row, and also to tell where the previous row created is located so
you know when enough space has gone by to create the next row.
"""
list_of_rows = []


def create_row():
    """This creates a list of icons. It does not display them to the screen."""
    global list_of_rows
    row = []
    for i in range(number_of_icons_in_a_row):
        n = randint(0, 350)
        if n == 350:
            energy = ghg_capture_technology
        elif n % 2 == 0:
            energy = choice(fossil_fuel_types)
        else:
            energy = choice(green_energy_types)
        icon = Icon(energy, first_x_coordinate + i * (64 + icon_spacing))
        row.append(icon)
    list_of_rows.append(row)
    return row


def display_row():
    """This creates a row of icons and displays them to the screen at the appropriate location."""
    global list_of_rows
    if len(list_of_rows) == 0:
        row = create_row()
        for icon in row:
            all_icons.add(icon)
    else:
        for i in range(number_of_icons_in_a_row):
            if list_of_rows[-1][i].rect.top < icon_spacing:
                pass
            else:
                row = create_row()
                for icon in row:
                    all_icons.add(icon)


running = True
frames = 0
fps_displayed = str(60)

fps_text = arial.render(fps_displayed + '/60', False, (0, 0, 0))
start_time = last_frame = time()

while running:
    frames += 1

    if frames%30 == 0: # update fps
        end_time = time()
        fps_displayed = str(int(30/(end_time-start_time)))
        fps_text = arial.render(fps_displayed + '/60', False, (0, 0, 0))
        start_time = time()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            icon_clicked(event)

    window.fill(white)

    display_row()

    all_icons.update()
    all_icons.draw(window)

    window.blit(fps_text,(0,0)) # fps

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
