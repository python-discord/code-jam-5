import pygame
from random import randint, choice
from assets import (
    natural_gas, oil, coal,
    solar, wind, hydro,
    geothermal, biomass, nuclear,
    hydrogen, ghg_capture_tech)  # Importing the images for the icons

# Details about the window:
window_width = 1152
aspect_ratio = 9 / 16
window_height = int(aspect_ratio * window_width)
window_icon = None
window_title = 'Iconic Energy, Inc.'

# Boiler-plate:
pygame.init()
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(window_title)
clock = pygame.time.Clock()
all_icons = pygame.sprite.Group()  # All icons on the screen are put into this Group object.

# Colors used:
white = (255, 255, 255)
gray = (124, 124, 124)
dark_red = (157, 49, 30)
yellow = (255, 255, 0)
black = (0, 0, 0)
darkish_brown = (81, 54, 26)
green = (0, 255, 0)
grayish_light_blue = (59, 131, 189)

# Fonts used:
pygame.font.init()
arial = pygame.font.SysFont('Arial MT', 30)
big_arial = pygame.font.SysFont('Arial', 120)

# Game settings:
fps = 60
icon_speed = 4  # Speed the icons fall at, y-pixels per frame.
number_of_icons_in_a_row = 8
icon_width = 64  # Width of the icons' images in pixels
num_ghg_capture_icons_per_minute = 3
greenhouse_gas_limit = 500000
energy_demand = 1000

"""
The following are the two energy types an icon can be, which energy sources
fall into those types, as well as a greenhouse gas capture technology type.
"""
fossil_fuel_types = (natural_gas, oil, coal)
green_energy_types = (solar, wind, hydro, geothermal,
                      biomass, nuclear, hydrogen)
ghg_capture_technology = ghg_capture_tech

# Initial game state values:
atmospheric_ghg_levels = 0

num_of_green_energies = 0
num_of_fossil_fuels = 50
num_of_ghg_capture_techs = 0

energy_output = 20 * num_of_fossil_fuels + num_of_green_energies
capture_offset = num_of_ghg_capture_techs

percent_fossil_fuel = 100
percent_green_energy = 0


def percentage_update():
    """Updates the percentage of energy resources that are fossil fuels and green energies"""
    total = (num_of_fossil_fuels + num_of_green_energies)

    global percent_fossil_fuel, percent_green_energy
    percent_fossil_fuel = int(100 * (num_of_fossil_fuels / total))
    percent_green_energy = int(100 * (num_of_green_energies / total))


def pollute():
    """Increase the amount of greenhouse gas in the atmosphere"""
    global atmospheric_ghg_levels
    atmospheric_ghg_levels += num_of_fossil_fuels


def check_if_lost():
    if atmospheric_ghg_levels >= greenhouse_gas_limit:
        return True
    elif energy_output < energy_demand:
        return True
    return False


def check_if_won():
    if percent_fossil_fuel <= capture_offset:
        return True
    return False


def draw_ghg_levels_bar():
    """Draws the Atmospheric GHG Levels stat bar onto the screen"""
    if atmospheric_ghg_levels <= greenhouse_gas_limit:
        pygame.draw.rect(window, gray,
                         pygame.Rect(icon_spacing,
                                     1.5 * icon_spacing,
                                     stat_bar_width,
                                     stat_bar_height))

        pygame.draw.rect(window, dark_red,
                         pygame.Rect(icon_spacing,
                                     1.5 * icon_spacing,
                                     stat_bar_width * atmospheric_ghg_levels / greenhouse_gas_limit,
                                     stat_bar_height))
    else:
        pygame.draw.rect(window, dark_red,
                         pygame.Rect(icon_spacing,
                                     1.5 * icon_spacing,
                                     stat_bar_width,
                                     stat_bar_height))

    text = arial.render('Atmospheric GHG Levels', False, (0, 0, 0))
    window.blit(text, (icon_spacing, 0.5 * icon_spacing))


def draw_energy_demand_bar():
    """Draws the Energy Demand stat bar onto the screen """
    if energy_output <= 2 * energy_demand:
        pygame.draw.rect(window, gray,
                         pygame.Rect(icon_spacing,
                                     1.5 * icon_spacing + window_height / 5,
                                     stat_bar_width,
                                     stat_bar_height))

        pygame.draw.rect(window, yellow,
                         pygame.Rect(icon_spacing,
                                     1.5 * icon_spacing + window_height / 5,
                                     (stat_bar_width / 2) * energy_output / energy_demand,
                                     stat_bar_height))
    else:
        pygame.draw.rect(window, yellow,
                         pygame.Rect(icon_spacing,
                                     1.5 * icon_spacing + window_height / 5,
                                     stat_bar_width,
                                     stat_bar_height))
    pygame.draw.rect(window, black,
                     pygame.Rect(icon_spacing + stat_bar_width / 2 - 2,
                                 1.5 * icon_spacing + window_height / 5 - 4,
                                 4,
                                 stat_bar_height + 8))

    text = arial.render('Energy Output & Demand', False, (0, 0, 0))
    window.blit(text, (icon_spacing, 0.5 * icon_spacing + window_height / 5))


def draw_ratio_bar():
    """Draws the Green Energy : Fossil Fuels ratio stat bar onto the screen"""
    pygame.draw.rect(window, darkish_brown,
                     pygame.Rect(icon_spacing,
                                 1.5 * icon_spacing + 2 * window_height / 5,
                                 stat_bar_width,
                                 stat_bar_height))

    pygame.draw.rect(window, green,
                     pygame.Rect(icon_spacing,
                                 1.5 * icon_spacing + 2 * window_height / 5,
                                 stat_bar_width * percent_green_energy / 100,
                                 stat_bar_height))

    text = arial.render('Green Energy : Fossil Fuels', False, (0, 0, 0))
    window.blit(text, (icon_spacing, 0.5 * icon_spacing + 2 * window_height / 5))


def draw_emission_offset_bar():
    """Draws the Emissions Offset stat bar onto the screen"""
    pygame.draw.rect(window, gray,
                     pygame.Rect(icon_spacing,
                                 1.5 * icon_spacing + 3 * window_height / 5,
                                 stat_bar_width,
                                 stat_bar_height))

    pygame.draw.rect(window, grayish_light_blue,
                     pygame.Rect(icon_spacing,
                                 1.5 * icon_spacing + 3 * window_height / 5,
                                 stat_bar_width * num_of_ghg_capture_techs / 100,
                                 stat_bar_height))

    text = arial.render('Emissions Offset', False, (0, 0, 0))
    window.blit(text, (icon_spacing, 0.5 * icon_spacing + 3 * window_height / 5))


def draw_stat_bars():
    """Draws all of the stat bars onto the screen and instructions to pause"""
    draw_ghg_levels_bar()
    draw_energy_demand_bar()
    draw_ratio_bar()
    draw_emission_offset_bar()
    text = arial.render('Press P to Pause', False, (0, 0, 0))
    window.blit(text, (icon_spacing + stat_bar_width / 4,
                       0.5 * icon_spacing + 4 * window_height / 5 + stat_bar_height / 2))


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
        elif energy_source in green_energy_types:
            self.type = 'green energy'
        elif energy_source == ghg_capture_tech:
            self.type = 'ghg capture tech'

    def update(self):
        """
        Every frame each icon falls down the screen at the specified
        speed. When it reaches the bottom it is removed.
        """
        self.rect.y += icon_speed
        if self.rect.top > window_height:
            self.kill()


def icon_clicked():
    """This runs if an icon is clicked."""
    global num_of_fossil_fuels, num_of_green_energies, num_of_ghg_capture_techs
    global energy_output, capture_offset

    if event.button == 1:  # Left-click
        if icon.type == 'fossil fuel':
            num_of_fossil_fuels += 1
            energy_output += 20
        elif icon.type == 'green energy':
            num_of_green_energies += 1
            energy_output += 1
        else:
            num_of_ghg_capture_techs += 1
            capture_offset += 1
        print([num_of_ghg_capture_techs, num_of_green_energies, num_of_fossil_fuels, energy_output])
        percentage_update()
        icon.kill()
    elif event.button == 3:  # Right-click
        if icon.type == 'fossil fuel' and num_of_fossil_fuels > 0:
            num_of_fossil_fuels -= 1
            energy_output -= 20
        elif icon.type == 'green energy' and num_of_green_energies > 0:
            num_of_green_energies -= 1
            energy_output -= 1
        elif num_of_ghg_capture_techs > 0:
            num_of_ghg_capture_techs -= 1
            capture_offset -= 1
        print([num_of_ghg_capture_techs, num_of_green_energies, num_of_fossil_fuels, energy_output])
        percentage_update()
        icon.kill()
    else:
        pass


"""
The following variables are used to generalize the spacing and layout of
the icons and stat bars relative to window size and the chosen number of
icons in a row. Hard coding in the positions of the icons and stat bars
would make future changes to window size or number of icons in a row
difficult because you would also have to go back and recalculate all the
icons' new positions.
"""
# Width of area containing the icons:
icon_area_width = 2 * window_width / 3

# Width of area containing the stat bars:
stat_area_width = window_width - icon_area_width

# Total amount of horizontal space between all icons in a row:
total_space_between_icons = icon_area_width - number_of_icons_in_a_row * icon_width

# Horizontal spacing between individual icons:
icon_spacing = total_space_between_icons / number_of_icons_in_a_row

# Width of the stat bars:
stat_bar_width = stat_area_width - 2 * icon_spacing

# Height of the stat bars:
stat_bar_height = window_height / 5 - 2 * icon_spacing

# The x-coordinate of the first icon in a row:
first_x_coordinate = window_width / 3

"""
The following variables are used to determine how rare a ghg_capture_tech
icon should be given an x desired amount of ghg_capture_tech icons per
minute (specified in game settings).
"""
# Time for an icon to fall to bottom of screen, in seconds:
time_for_icon_to_fall = (window_height / icon_speed) / fps

# How many icons are on screen at any point in time (except in the beginning):
num_of_icons_on_screen = window_height / (icon_width + icon_spacing) * number_of_icons_in_a_row

# How many icons are shown on the screen in one minute:
num_of_icons_shown_in_one_minute = (60 / time_for_icon_to_fall) * num_of_icons_on_screen

# Rarity of the ghg capture icon,
# i.e. how many icons go by on the screen (on average) before you see one:
ghg_capture_icon_rarity = int(num_of_icons_shown_in_one_minute / num_ghg_capture_icons_per_minute)

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
        n = randint(0, ghg_capture_icon_rarity)
        if n == ghg_capture_icon_rarity:
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


# Used to make an FPS counter:
frames = 0
fps_text = arial.render('FPS: ?/60', False, (0, 0, 0))  # FPS counter text on screen


def fps_counter():
    """Displays an FPS counter on the screen"""
    global frames, fps_text
    if frames % 10 == 0:  # Update FPS counter on screen every 10 frames
        fps_displayed = str(int(clock.get_fps()))
        fps_text = arial.render(f'FPS: {fps_displayed}/60', False, (0, 0, 0))
    window.blit(fps_text, (0, window_height - 20))


def tutorial():
    """Credit goes to https://docs.opencv.org/master/dd/d43/tutorial_py_video_display.html"""
    import cv2

    cap = cv2.VideoCapture('assets/tutorial.mov')

    while(cap.isOpened()):
        ret, frame = cap.read()

        if not ret or cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow('frame', frame)

    cap.release()
    cv2.destroyAllWindows()

# test if the tutorial needs to be played


try:
    tutorial_file = open('saves/tutorial.txt')  # error causing function 1

    tutorial_content = tutorial_file.read()
    tutorial_file.close()
    del tutorial_file

    assert tutorial_content == 'done'  # error causing function 2

except Exception:
    tutorial()
    with open('saves/tutorial.txt', 'w') as f:
        f.write('done')


pause = False
running = True
tint = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            for icon in all_icons:
                if icon.rect.collidepoint(mouse_position):
                    icon_clicked()

        # Pause sequence:
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                pause = True

        while pause:
            for event2 in pygame.event.get():
                if event2.type == pygame.KEYUP:
                    if event2.key == pygame.K_p:
                        pause = False
                elif event2.type == pygame.QUIT:
                    pause = False
                    running = False

    window.fill(white)

    pollute()

    display_row()
    draw_stat_bars()

    all_icons.update()
    all_icons.draw(window)
    fps_counter()

    frames += 1

    pygame.display.update()

    if check_if_lost() or check_if_won():
        pause = True  # pause the game
        pygame.display.update()

        if check_if_lost():
            color = '(255-(64*tint), 255-(192*tint), 255-(255*tint))'
        elif check_if_won():
            color = '(255-(255*tint), 255, 255-(128*tint))'
        else:  # u wOT
            continue

        tint = 0
        while tint <= 1:
            window.fill(eval(color), special_flags=pygame.BLEND_MULT)
            pygame.display.update()
            tint += 0.05
            clock.tick(fps)

        from_color = eval(color)

        tint = 0
        while tint <= 1:
            window.fill(eval(color))
            pygame.display.update()
            tint += 0.1
            clock.tick(fps)

        text = 'You '
        if check_if_lost():
            text += 'lost...'
        elif check_if_won():
            text += 'won!'
        else:  # u wOT
            continue

        ending_text = big_arial.render(text, False, (0, 0, 0))
        window.blit(ending_text, (100, 100))
        pygame.display.update()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    clock.tick(fps)

pygame.quit()
