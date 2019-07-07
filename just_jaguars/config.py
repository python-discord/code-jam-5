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

# Game settings:
fps = 60
icon_speed = 4  # Speed the icons fall at, y-pixels per frame.
number_of_icons_in_a_row = 8
icon_width = 64  # Width of the icons' images in pixels
num_ghg_capture_icons_per_minute = 3
greenhouse_gas_limit = 500000
energy_demand = 1000

# Colors used:
white = (255, 255, 255)
gray = (124, 124, 124)
dark_red = (157, 49, 30)
yellow = (255, 255, 0)
black = (0, 0, 0)
darkish_brown = (81, 54, 26)
green = (0, 255, 0)
grayish_light_blue = (59, 131, 189)

"""
The following are the two energy types an icon can be, which energy sources
fall into those types, as well as a greenhouse gas capture technology type.
"""
fossil_fuel_types = (natural_gas, oil, coal)
green_energy_types = (solar, wind, hydro, geothermal,
                      biomass, nuclear, hydrogen)
ghg_capture_technology = ghg_capture_tech

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
