import pygame
from random import randint, choice
import config

# tutorial:
import tutorial
tutorial.__dict__  # because flake8 ;-;

# Boiler-plate:
pygame.init()
window = pygame.display.set_mode((config.window_width, config.window_height))
pygame.display.set_caption(config.window_title)
clock = pygame.time.Clock()
all_icons = pygame.sprite.Group()  # All icons on the screen are put into this Group object.

# Fonts used:
pygame.font.init()
arial = pygame.font.SysFont('Arial MT', 30)
big_arial = pygame.font.SysFont('Arial', 120)

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
    if atmospheric_ghg_levels >= config.greenhouse_gas_limit:
        return True
    elif energy_output < config.energy_demand:
        return True
    return False


def check_if_won():
    if percent_fossil_fuel <= capture_offset:
        return True
    return False


def draw_ghg_levels_bar():
    """Draws the Atmospheric GHG Levels stat bar onto the screen"""
    if atmospheric_ghg_levels <= config.greenhouse_gas_limit:
        pygame.draw.rect(window, config.gray,
                         pygame.Rect(config.icon_spacing,
                                     1.5 * config.icon_spacing,
                                     config.stat_bar_width,
                                     config.stat_bar_height))

        pygame.draw.rect(window, config.dark_red,
                         pygame.Rect(config.icon_spacing,
                                     1.5 * config.icon_spacing,
                                     (config.stat_bar_width * atmospheric_ghg_levels)
                                     / config.greenhouse_gas_limit,
                                     config.stat_bar_height))
    else:
        pygame.draw.rect(window, config.dark_red,
                         pygame.Rect(config.icon_spacing,
                                     1.5 * config.icon_spacing,
                                     config.stat_bar_width,
                                     config.stat_bar_height))

    text = arial.render('Atmospheric GHG Levels', False, (0, 0, 0))
    window.blit(text, (config.icon_spacing, 0.5 * config.icon_spacing))


def draw_energy_demand_bar():
    """Draws the Energy Demand stat bar onto the screen """
    if energy_output <= 2 * config.energy_demand:
        pygame.draw.rect(window, config.gray,
                         pygame.Rect(config.icon_spacing,
                                     1.5 * config.icon_spacing + config.window_height / 5,
                                     config.stat_bar_width,
                                     config.stat_bar_height))

        pygame.draw.rect(window, config.yellow,
                         pygame.Rect(config.icon_spacing,
                                     1.5 * config.icon_spacing + config.window_height / 5,
                                     (config.stat_bar_width / 2)
                                     * energy_output / config.energy_demand,
                                     config.stat_bar_height))
    else:
        pygame.draw.rect(window, config.yellow,
                         pygame.Rect(config.icon_spacing,
                                     1.5 * config.icon_spacing + config.window_height / 5,
                                     config.stat_bar_width,
                                     config.stat_bar_height))
    pygame.draw.rect(window, config.black,
                     pygame.Rect(config.icon_spacing + config.stat_bar_width / 2 - 2,
                                 1.5 * config.icon_spacing + config.window_height / 5 - 4,
                                 4,
                                 config.stat_bar_height + 8))

    text = arial.render('Energy Output & Demand', False, (0, 0, 0))
    window.blit(text, (config.icon_spacing, 0.5 * config.icon_spacing + config.window_height / 5))


def draw_ratio_bar():
    """Draws the Green Energy : Fossil Fuels ratio stat bar onto the screen"""
    pygame.draw.rect(window, config.darkish_brown,
                     pygame.Rect(config.icon_spacing,
                                 1.5 * config.icon_spacing + 2 * config.window_height / 5,
                                 config.stat_bar_width,
                                 config.stat_bar_height))

    pygame.draw.rect(window, config.green,
                     pygame.Rect(config.icon_spacing,
                                 1.5 * config.icon_spacing + 2 * config.window_height / 5,
                                 config.stat_bar_width * percent_green_energy / 100,
                                 config.stat_bar_height))

    text = arial.render('Green Energy : Fossil Fuels', False, (0, 0, 0))
    window.blit(text, (config.icon_spacing, 0.5 *
                config.icon_spacing + 2 * config.window_height / 5))


def draw_emission_offset_bar():
    """Draws the Emissions Offset stat bar onto the screen"""
    pygame.draw.rect(window, config.gray,
                     pygame.Rect(config.icon_spacing,
                                 1.5 * config.icon_spacing + 3 * config.window_height / 5,
                                 config.stat_bar_width,
                                 config.stat_bar_height))

    pygame.draw.rect(window, config.grayish_light_blue,
                     pygame.Rect(config.icon_spacing,
                                 1.5 * config.icon_spacing + 3 * config.window_height / 5,
                                 config.stat_bar_width * num_of_ghg_capture_techs / 100,
                                 config.stat_bar_height))

    text = arial.render('Emissions Offset', False, (0, 0, 0))
    window.blit(text, (config.icon_spacing, 0.5 *
                config.icon_spacing + 3 * config.window_height / 5))


def draw_stat_bars():
    """Draws all of the stat bars onto the screen and instructions to pause"""
    draw_ghg_levels_bar()
    draw_energy_demand_bar()
    draw_ratio_bar()
    draw_emission_offset_bar()
    text = arial.render('Press P to Pause', False, (0, 0, 0))
    window.blit(text, (config.icon_spacing + config.stat_bar_width / 4,
                       0.5 * config.icon_spacing + 4 * config.window_height / 5
                       + config.stat_bar_height / 2))


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
        if energy_source in config.fossil_fuel_types:
            self.type = 'fossil fuel'
        elif energy_source in config.green_energy_types:
            self.type = 'green energy'
        elif energy_source == config.ghg_capture_tech:
            self.type = 'ghg capture tech'

    def update(self):
        """
        Every frame each icon falls down the screen at the specified
        speed. When it reaches the bottom it is removed.
        """
        self.rect.y += config.icon_speed
        if self.rect.top > config.window_height:
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
This list keeps track of all the rows created. It is used to create the
first row, and also to tell where the previous row created is located so
you know when enough space has gone by to create the next row.
"""
list_of_rows = []


def create_row():
    """This creates a list of icons. It does not display them to the screen."""
    global list_of_rows
    row = []
    for i in range(config.number_of_icons_in_a_row):
        n = randint(0, config.ghg_capture_icon_rarity)
        if n == config.ghg_capture_icon_rarity:
            energy = config.ghg_capture_technology
        elif n % 2 == 0:
            energy = choice(config.fossil_fuel_types)
        else:
            energy = choice(config.green_energy_types)
        icon = Icon(energy, config.first_x_coordinate + i * (64 + config.icon_spacing))
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
        for i in range(config.number_of_icons_in_a_row):
            if list_of_rows[-1][i].rect.top < config.icon_spacing:
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
    window.blit(fps_text, (0, config.window_height - 20))


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

    window.fill(config.white)

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
            clock.tick(config.fps)

        from_color = eval(color)

        tint = 0
        while tint <= 1:
            window.fill(eval(color))
            pygame.display.update()
            tint += 0.1
            clock.tick(config.fps)

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

    clock.tick(config.fps)

pygame.quit()
